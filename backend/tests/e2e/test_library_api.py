import pytest

pytestmark = pytest.mark.e2e


async def test_list_library_unauthenticated_returns_403(http_client):
    r = await http_client.get("/api/library")
    assert r.status_code == 403


async def test_list_published_pieces(http_client, learner_cookie, seed_published_piece):
    await seed_published_piece(slug="coastlines", title="Coastlines")
    r = await http_client.get("/api/library", cookies=learner_cookie)
    assert r.status_code == 200
    body = r.json()
    assert any(item["slug"] == "coastlines" for item in body["items"])


async def test_get_piece_by_slug(http_client, learner_cookie, seed_published_piece):
    await seed_published_piece(slug="coastlines")
    r = await http_client.get("/api/library/coastlines", cookies=learner_cookie)
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "coastlines"
    assert body["body"]["kind"] == "reading"


async def test_draft_piece_returns_404_from_public_endpoint(http_client, learner_cookie, seed_draft_piece):
    await seed_draft_piece(slug="secret")
    r = await http_client.get("/api/library/secret", cookies=learner_cookie)
    assert r.status_code == 404
