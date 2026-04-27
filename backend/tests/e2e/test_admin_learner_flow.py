import pytest

pytestmark = pytest.mark.e2e


async def test_admin_publishes_learner_sees(http_client, admin_cookie, learner_cookie):
    create = await http_client.post(
        "/api/admin/content",
        json={
            "kind": "reading",
            "slug": "smoke-piece",
            "title": "Smoke",
            "cefr": "B1",
            "minutes": 5,
            "topic": "travel",
            "body": {
                "kind": "reading",
                "text": "x" * 200,
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
        cookies=admin_cookie,
    )
    assert create.status_code == 201, create.text
    pid = create.json()["id"]

    pub = await http_client.post(f"/api/admin/content/{pid}/publish", cookies=admin_cookie)
    assert pub.status_code == 200, pub.text

    r = await http_client.get("/api/library/smoke-piece", cookies=learner_cookie)
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "published"
