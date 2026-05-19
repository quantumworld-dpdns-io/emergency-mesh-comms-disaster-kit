from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app


def _auth_headers(client: TestClient, admin: bool = False) -> dict[str, str]:
    resp = client.post("/api/v1/auth/token", params={"node_id": "node-test", "admin": admin})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_bundle_submit_and_status() -> None:
    with TestClient(app) as client:
        headers = _auth_headers(client)
        created = client.post(
            "/api/v1/bundles",
            headers=headers,
            json={"destination_eid": "dtn://node-2", "payload": "hello", "priority": "general"},
        )
        assert created.status_code == 200
        bundle_id = created.json()["bundle_id"]

        fetched = client.get(f"/api/v1/bundles/{bundle_id}", headers=headers)
        assert fetched.status_code == 200
        assert fetched.json()["status"] == "queued"


def test_message_send_requires_api_key() -> None:
    with TestClient(app) as client:
        headers = _auth_headers(client)
        denied = client.post(
            "/api/v1/messages",
            headers=headers,
            json={"to_eid": "dtn://node-2", "text": "hi", "priority": "general"},
        )
        assert denied.status_code == 401

        allowed = client.post(
            "/api/v1/messages",
            headers={**headers, "X-API-Key": "dev-api-key"},
            json={"to_eid": "dtn://node-2", "text": "hi", "priority": "general"},
        )
        assert allowed.status_code == 200


def test_admin_emergency_endpoint() -> None:
    with TestClient(app) as client:
        user_headers = _auth_headers(client, admin=False)
        forbidden = client.post("/api/v1/emergency", headers=user_headers, params={"message": "SOS"})
        assert forbidden.status_code == 403

        admin_headers = _auth_headers(client, admin=True)
        ok = client.post("/api/v1/emergency", headers=admin_headers, params={"message": "SOS"})
        assert ok.status_code == 200
        assert ok.json()["status"] == "broadcasted"
