from fastapi.testclient import TestClient

from src.api.main import app


def test_health_headers() -> None:
    with TestClient(app) as c:
        r = c.get("/healthz")
        assert r.status_code == 200
        assert "x-content-type-options" in {k.lower() for k in r.headers.keys()}
