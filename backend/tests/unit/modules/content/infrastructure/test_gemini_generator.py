from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.modules.content.application.dto import GenerationSpec
from app.modules.content.domain.exceptions import GenerationFailed
from app.modules.content.domain.value_objects import CefrLevel, PieceKind, Topic
from app.modules.content.infrastructure.generation.gemini_generator import (
    GeminiContentGenerator,
)


def _resp(tool_input: dict, usage: dict | None = None):
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "function_call": {
                                "name": "create_piece_draft",
                                "args": tool_input,
                            }
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {
            "promptTokenCount": (usage or {}).get("input_tokens", 10),
            "candidatesTokenCount": (usage or {}).get("output_tokens", 5),
        },
    }


def _reading_payload():
    return {
        "kind": "reading",
        "slug": "coastal-winds",
        "title": "Coastal Winds",
        "minutes": 6,
        "body": {
            "text": "x" * 300,
            "mcq": [
                {
                    "question": f"Q{i}",
                    "choices": ["a", "b", "c"],
                    "correct_index": 0,
                    "rationale": "r",
                }
                for i in range(3)
            ],
            "short_answer": {"prompt": "Summarize", "grading_notes": "n"},
        },
    }


@pytest.mark.asyncio
async def test_generate_draft_happy_path():
    generate_content = AsyncMock(return_value=_resp(_reading_payload()))
    client = SimpleNamespace(generate_content=generate_content)
    gen = GeminiContentGenerator(client=client, model="gemini-2.5-flash")
    piece = await gen.generate_draft(
        GenerationSpec(
            kind=PieceKind.READING,
            cefr=CefrLevel.B1,
            topic=Topic.SCIENCE,
            seed_prompt=None,
        )
    )
    assert piece.source.value == "llm_generated"
    assert piece.slug.value == "coastal-winds"
    assert piece.generation_metadata["model"] == "gemini-2.5-flash"
    assert "prompt_hash" in piece.generation_metadata
    assert piece.generation_metadata["usage"] == {"input_tokens": 10, "output_tokens": 5}


@pytest.mark.asyncio
async def test_invalid_output_retries_once_then_fails():
    bad = _resp({"kind": "reading", "slug": "", "title": "", "minutes": 1, "body": {"text": "short"}})
    generate_content = AsyncMock(side_effect=[bad, bad])
    client = SimpleNamespace(generate_content=generate_content)
    gen = GeminiContentGenerator(client=client, model="m")
    with pytest.raises(GenerationFailed) as exc:
        await gen.generate_draft(
            GenerationSpec(
                kind=PieceKind.READING,
                cefr=CefrLevel.B1,
                topic=Topic.SCIENCE,
                seed_prompt=None,
            )
        )
    assert generate_content.call_count == 2
    assert exc.value.reason == "invalid_output"
    assert exc.value.details


@pytest.mark.asyncio
async def test_retry_recovers():
    bad = _resp({"kind": "reading", "slug": "", "title": "", "minutes": 1, "body": {"text": "short"}})
    good = _resp(_reading_payload())
    generate_content = AsyncMock(side_effect=[bad, good])
    client = SimpleNamespace(generate_content=generate_content)
    gen = GeminiContentGenerator(client=client, model="m")
    piece = await gen.generate_draft(
        GenerationSpec(
            kind=PieceKind.READING,
            cefr=CefrLevel.B1,
            topic=Topic.SCIENCE,
            seed_prompt=None,
        )
    )
    assert piece.slug.value == "coastal-winds"
    assert generate_content.call_count == 2
