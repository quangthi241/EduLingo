from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.e2e


def _tool_response(kind: str = "reading"):
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "function_call": {
                                "name": "create_piece_draft",
                                "args": {
                                    "kind": kind,
                                    "slug": "generated-piece",
                                    "title": "Generated Piece",
                                    "minutes": 6,
                                    "body": {
                                        "text": "x" * 300,
                                        "mcq": [
                                            {
                                                "question": f"Q{i}",
                                                "choices": ["a", "b"],
                                                "correct_index": 0,
                                                "rationale": "r",
                                            }
                                            for i in range(3)
                                        ],
                                        "short_answer": {"prompt": "p", "grading_notes": "n"},
                                    },
                                },
                            }
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 8},
    }


def _stub_gemini(tool_response):
    async def _generate_content(**kwargs):
        return tool_response

    def _factory(**kw):
        return SimpleNamespace(generate_content=_generate_content)

    return _factory


async def test_generate_happy_path(http_client, admin_cookie, monkeypatch):
    monkeypatch.setattr("app.container.GeminiApiClient", _stub_gemini(_tool_response()))
    r = await http_client.post(
        "/api/admin/content/generate",
        json={"kind": "reading", "cefr": "B1", "topic": "science"},
        cookies=admin_cookie,
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["source"] == "llm_generated"
    assert body["slug"] == "generated-piece"


async def test_generate_invalid_returns_502(http_client, admin_cookie, monkeypatch):
    bad = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "function_call": {
                                "name": "create_piece_draft",
                                "args": {
                                    "kind": "reading",
                                    "slug": "",
                                    "title": "",
                                    "minutes": 1,
                                    "body": {"text": "short"},
                                },
                            }
                        }
                    ]
                }
            }
        ],
        "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1},
    }
    monkeypatch.setattr("app.container.GeminiApiClient", _stub_gemini(bad))
    r = await http_client.post(
        "/api/admin/content/generate",
        json={"kind": "reading", "cefr": "B1", "topic": "science"},
        cookies=admin_cookie,
    )
    assert r.status_code == 502, r.text
    assert "details" in r.json()


async def test_generate_rate_limited(http_client, admin_cookie, monkeypatch):
    monkeypatch.setattr("app.container.GeminiApiClient", _stub_gemini(_tool_response()))
    # Fire 10 requests — the first creates the piece (201); subsequent calls
    # fail on slug collision (caught by the use case as GenerationFailed → 502,
    # OR surface directly as SlugAlreadyExists → 409, depending on use-case
    # internals). Either way the rate-limit bucket fills to 10.
    for _ in range(10):
        r = await http_client.post(
            "/api/admin/content/generate",
            json={"kind": "reading", "cefr": "B1", "topic": "science"},
            cookies=admin_cookie,
        )
        assert r.status_code in (201, 409, 502), r.text

    # 11th request exceeds 10-per-minute window.
    r11 = await http_client.post(
        "/api/admin/content/generate",
        json={"kind": "reading", "cefr": "B1", "topic": "science"},
        cookies=admin_cookie,
    )
    assert r11.status_code == 429, r11.text
    assert "Retry-After" in r11.headers
