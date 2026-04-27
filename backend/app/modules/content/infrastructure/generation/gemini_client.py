from __future__ import annotations

from typing import Any

import httpx


class GeminiApiClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout_seconds: float = 45.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    async def generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        body: dict[str, Any] = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": str(config.get("system_instruction", ""))}],
            },
            "tools": config.get("tools", []),
            "toolConfig": config.get("tool_config", {}),
        }

        endpoint = f"{self._base_url}/models/{model}:generateContent"
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            response = await client.post(endpoint, params={"key": self._api_key}, json=body)
            response.raise_for_status()
            return response.json()
