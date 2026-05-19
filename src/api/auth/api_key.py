from __future__ import annotations

import hashlib
import hmac

from fastapi import Header, HTTPException, Request


class APIKeyManager:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    @staticmethod
    def _hash(api_key: str) -> str:
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    def add_key(self, client_id: str, api_key: str) -> None:
        self._store[client_id] = self._hash(api_key)

    def verify(self, api_key: str) -> bool:
        hashed = self._hash(api_key)
        return any(hmac.compare_digest(hashed, v) for v in self._store.values())


api_key_manager = APIKeyManager()
api_key_manager.add_key("default-device", "dev-api-key")


async def require_api_key(request: Request, x_api_key: str = Header(default="")) -> str:
    if x_api_key and api_key_manager.verify(x_api_key):
        request.state.api_client = "device"
        return "device"
    raise HTTPException(status_code=401, detail="invalid api key")
