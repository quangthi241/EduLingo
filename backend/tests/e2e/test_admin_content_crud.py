import pytest

pytestmark = pytest.mark.e2e


async def test_non_admin_blocked(http_client, learner_cookie):
    r = await http_client.get("/api/admin/content", cookies=learner_cookie)
    assert r.status_code == 403


async def test_admin_crud_lifecycle(http_client, admin_cookie):
    create = await http_client.post(
        "/api/admin/content",
        json={
            "kind": "reading",
            "slug": "crud-test",
            "title": "CRUD Test",
            "cefr": "B1",
            "minutes": 6,
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

    patch = await http_client.patch(
        f"/api/admin/content/{pid}",
        json={"title": "Renamed"},
        cookies=admin_cookie,
    )
    assert patch.status_code == 200, patch.text
    assert patch.json()["title"] == "Renamed"

    pub = await http_client.post(f"/api/admin/content/{pid}/publish", cookies=admin_cookie)
    assert pub.status_code == 200, pub.text
    assert pub.json()["status"] == "published"

    arch = await http_client.post(f"/api/admin/content/{pid}/archive", cookies=admin_cookie)
    assert arch.status_code == 200, arch.text
    assert arch.json()["status"] == "archived"


async def test_admin_get_piece_by_id(http_client, admin_cookie):
    create = await http_client.post(
        "/api/admin/content",
        json={
            "kind": "reading",
            "slug": "get-by-id",
            "title": "Get By Id",
            "cefr": "B1",
            "minutes": 6,
            "topic": "science",
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

    get_one = await http_client.get(f"/api/admin/content/{pid}", cookies=admin_cookie)
    assert get_one.status_code == 200, get_one.text
    body = get_one.json()
    assert body["id"] == pid
    assert body["slug"] == "get-by-id"


async def test_duplicate_slug_returns_409(http_client, admin_cookie):
    payload = {
        "kind": "reading",
        "slug": "dup",
        "title": "dup",
        "cefr": "B1",
        "minutes": 5,
        "topic": "travel",
        "body": {
            "kind": "reading",
            "text": "x" * 200,
            "mcq": [
                {
                    "question": "Q",
                    "choices": ["a", "b"],
                    "correctIndex": 0,
                    "rationale": "r",
                }
                for _ in range(3)
            ],
            "shortAnswer": {"prompt": "p", "gradingNotes": "n"},
        },
    }
    r1 = await http_client.post("/api/admin/content", json=payload, cookies=admin_cookie)
    assert r1.status_code == 201, r1.text
    r2 = await http_client.post("/api/admin/content", json=payload, cookies=admin_cookie)
    assert r2.status_code == 409, r2.text


async def test_delete_published_rejected(http_client, admin_cookie, seed_published_piece):
    piece = await seed_published_piece(slug="del-me")
    r = await http_client.delete(f"/api/admin/content/{piece['id']}", cookies=admin_cookie)
    assert r.status_code == 422, r.text


async def test_invalid_reading_payload_returns_422_not_500(http_client, admin_cookie):
    r = await http_client.post(
        "/api/admin/content",
        json={
            "kind": "reading",
            "slug": "bad-reading",
            "title": "Bad Reading",
            "cefr": "B1",
            "minutes": 6,
            "topic": "travel",
            "body": {
                "kind": "reading",
                "text": "too short",
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
    assert r.status_code == 422, r.text
    payload = r.json()
    assert payload["title"] == "validation_error"
    assert "reading text must be 100..4000 chars" in payload["detail"]
