from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.modules.content.application.body_builder import build_body
from app.modules.content.application.dto import GenerationSpec
from app.modules.content.application.ports import ContentGenerator
from app.modules.content.domain.entities import Piece
from app.modules.content.domain.exceptions import ContentError, GenerationFailed
from app.modules.content.domain.value_objects import (
    PieceKind,
    PieceSource,
    Slug,
)
from app.modules.content.infrastructure.generation.tool_schema import (
    CREATE_PIECE_DRAFT_TOOL,
)

_SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "system.md"


def _load_system_prompt() -> str:
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class GeminiContentGenerator(ContentGenerator):
    def __init__(self, *, client: Any, model: str) -> None:
        self._client = client
        self._model = model
        self._system_prompt = _load_system_prompt()

    def _user_prompt(self, spec: GenerationSpec) -> str:
        parts = [
            f"Kind: {spec.kind.value}",
            f"CEFR: {spec.cefr.value}",
            f"Topic: {spec.topic.value}",
        ]
        if spec.seed_prompt:
            parts.append(f"Seed: {spec.seed_prompt}")
        return "\n".join(parts)

    def _extract_tool_input(self, response: Any) -> dict[str, Any]:
        candidates = _get(response, "candidates", [])
        for candidate in candidates:
            content = _get(candidate, "content")
            if content is None:
                continue
            for part in _get(content, "parts", []):
                function_call = _get(part, "function_call") or _get(part, "functionCall")
                if function_call is None:
                    continue
                if _get(function_call, "name") != "create_piece_draft":
                    continue
                args = _get(function_call, "args")
                if isinstance(args, dict):
                    return args
                if isinstance(args, str):
                    parsed = json.loads(args)
                    if isinstance(parsed, dict):
                        return parsed
        raise GenerationFailed("upstream", ["no function call for create_piece_draft in response"])

    def _extract_usage(self, response: Any) -> dict[str, int]:
        usage = _get(response, "usage_metadata") or _get(response, "usageMetadata") or {}
        return {
            "input_tokens": int(
                _get(usage, "prompt_token_count", _get(usage, "promptTokenCount", 0)) or 0
            ),
            "output_tokens": int(
                _get(usage, "candidates_token_count", _get(usage, "candidatesTokenCount", 0)) or 0
            ),
        }

    async def _call(self, contents: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, int]]:
        try:
            response = await self._client.generate_content(
                model=self._model,
                contents=contents,
                config={
                    "system_instruction": self._system_prompt,
                    "tools": [
                        {
                            "functionDeclarations": [
                                {
                                    "name": CREATE_PIECE_DRAFT_TOOL["name"],
                                    "description": CREATE_PIECE_DRAFT_TOOL["description"],
                                    "parameters": CREATE_PIECE_DRAFT_TOOL["input_schema"],
                                }
                            ]
                        }
                    ],
                    "tool_config": {
                        "functionCallingConfig": {
                            "mode": "ANY",
                            "allowedFunctionNames": ["create_piece_draft"],
                        }
                    },
                },
            )
        except GenerationFailed:
            raise
        except Exception as e:
            raise GenerationFailed("upstream", [str(e)]) from e
        return self._extract_tool_input(response), self._extract_usage(response)

    def _build_piece(
        self, spec: GenerationSpec, payload: dict[str, Any], prompt_hash: str, usage: dict[str, int]
    ) -> Piece:
        kind = PieceKind(payload["kind"])
        if kind != spec.kind:
            raise GenerationFailed("invalid_output", [f"kind mismatch: {payload['kind']}"])
        now = datetime.now(UTC)
        body = build_body(kind, payload["body"])
        return Piece(
            id=uuid4(),
            slug=Slug(payload["slug"]),
            title=payload["title"],
            cefr=spec.cefr,
            minutes=payload["minutes"],
            kind=kind,
            topic=spec.topic,
            source=PieceSource.LLM_GENERATED,
            body=body,
            created_at=now,
            updated_at=now,
            generation_metadata={
                "model": self._model,
                "prompt_hash": prompt_hash,
                "generated_at": now.isoformat(),
                "usage": usage,
            },
        )

    async def generate_draft(self, spec: GenerationSpec) -> Piece:
        spec_json = json.dumps(
            {
                "kind": spec.kind.value,
                "cefr": spec.cefr.value,
                "topic": spec.topic.value,
                "seed_prompt": spec.seed_prompt,
            },
            sort_keys=True,
        )
        prompt_hash = hashlib.sha256(spec_json.encode()).hexdigest()

        user_prompt = self._user_prompt(spec)
        first_contents: list[dict[str, Any]] = [{"role": "user", "parts": [{"text": user_prompt}]}]

        first_payload, first_usage = await self._call(first_contents)
        try:
            return self._build_piece(spec, first_payload, prompt_hash, first_usage)
        except (ContentError, ValueError, KeyError) as e:
            errs = [str(e)]

        second_contents: list[dict[str, Any]] = [
            {"role": "user", "parts": [{"text": user_prompt}]},
            {
                "role": "model",
                "parts": [
                    {
                        "functionCall": {
                            "name": "create_piece_draft",
                            "args": first_payload,
                        }
                    }
                ],
            },
            {
                "role": "user",
                "parts": [
                    {
                        "functionResponse": {
                            "name": "create_piece_draft",
                            "response": {
                                "error": (
                                    "Invalid output. Fix these issues and return a valid "
                                    "create_piece_draft function call:\n- " + "\n- ".join(errs)
                                )
                            },
                        }
                    }
                ],
            },
        ]
        second_payload, second_usage = await self._call(second_contents)
        try:
            return self._build_piece(spec, second_payload, prompt_hash, second_usage)
        except (ContentError, ValueError, KeyError) as e:
            raise GenerationFailed("invalid_output", [*errs, str(e)]) from e
