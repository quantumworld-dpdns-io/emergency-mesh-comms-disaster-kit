from __future__ import annotations

import requests


class MeshLibrary:
    def __init__(self, base_url: str = "http://localhost:8080") -> None:
        self.base_url = base_url

    def send_bundle(self, token: str, destination_eid: str, payload: str) -> dict:
        r = requests.post(
            f"{self.base_url}/api/v1/bundles",
            headers={"Authorization": f"Bearer {token}"},
            json={"destination_eid": destination_eid, "payload": payload, "priority": "general"},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
