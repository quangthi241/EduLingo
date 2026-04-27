import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.shared.errors import NotFoundError, install_exception_handlers


@pytest.mark.unit
def test_not_found_error_maps_to_404_problem_json() -> None:
    app = FastAPI()
    install_exception_handlers(app)

    @app.get("/x")
    async def x() -> None:
        raise NotFoundError("user 42 not found")

    r = TestClient(app).get("/x")
    assert r.status_code == 404
    body = r.json()
    assert body["status"] == 404
    assert body["type"] == "about:blank"
    assert body["title"] == "not_found"
    assert body["detail"] == "user 42 not found"
