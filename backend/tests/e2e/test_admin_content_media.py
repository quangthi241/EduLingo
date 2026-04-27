import pytest

pytestmark = pytest.mark.e2e


async def _create_listening_draft(http_client, cookies):
    r = await http_client.post(
        "/api/admin/content",
        json={
            "kind": "listening",
            "slug": "audio-draft",
            "title": "Audio Draft",
            "cefr": "B1",
            "minutes": 5,
            "topic": "culture",
            "body": {
                "kind": "listening",
                "audioRef": None,
                "transcript": "t",
                "mcq": [
                    {
                        "question": f"Q{i}",
                        "choices": ["a", "b"],
                        "correctIndex": 0,
                        "rationale": "r",
                    }
                    for i in range(3)
                ],
                "shortAnswer": {"prompt": "p", "gradingNotes": "n"},
            },
        },
        cookies=cookies,
    )
    assert r.status_code == 201, r.text
    return r.json()


async def test_upload_audio_attaches_ref(http_client, admin_cookie):
    piece = await _create_listening_draft(http_client, admin_cookie)
    files = {"file": ("audio.mp3", b"\xff\xfe audio bytes", "audio/mpeg")}
    r = await http_client.post(
        f"/api/admin/content/{piece['id']}/media",
        files=files,
        cookies=admin_cookie,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["body"]["audioRef"] is not None
    assert body["body"]["audioRef"]["mimeType"] == "audio/mpeg"


async def test_upload_on_reading_rejected(http_client, admin_cookie, seed_draft_piece):
    draft = await seed_draft_piece(slug="wrong-kind")
    files = {"file": ("a.mp3", b"x", "audio/mpeg")}
    r = await http_client.post(f"/api/admin/content/{draft['id']}/media", files=files, cookies=admin_cookie)
    assert r.status_code == 422, r.text
