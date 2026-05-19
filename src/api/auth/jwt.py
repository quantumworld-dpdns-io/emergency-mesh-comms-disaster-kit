from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from fastapi import Depends, Header, HTTPException


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


@dataclass(slots=True)
class NodePrincipal:
    node_id: str
    is_admin: bool


class JWTManager:
    def __init__(self, private_key_pem: bytes | None = None, public_key_pem: bytes | None = None) -> None:
        self._private = (
            load_pem_private_key(private_key_pem, password=None)
            if private_key_pem
            else Ed25519PrivateKey.generate()
        )
        self._public = (
            load_pem_public_key(public_key_pem)
            if public_key_pem
            else self._private.public_key()
        )

    def issue(self, node_id: str, is_admin: bool = False, ttl_seconds: int = 3600) -> str:
        header = {"alg": "EdDSA", "typ": "JWT"}
        now = int(time.time())
        payload = {"sub": node_id, "admin": is_admin, "iat": now, "exp": now + ttl_seconds}
        h = _b64url(json.dumps(header, separators=(",", ":")).encode())
        p = _b64url(json.dumps(payload, separators=(",", ":")).encode())
        signing_input = f"{h}.{p}".encode("ascii")
        if not isinstance(self._private, Ed25519PrivateKey):
            raise TypeError("invalid private key type")
        sig = self._private.sign(signing_input)
        return f"{h}.{p}.{_b64url(sig)}"

    def verify(self, token: str) -> NodePrincipal:
        try:
            h, p, s = token.split(".")
            signing_input = f"{h}.{p}".encode("ascii")
            payload = json.loads(_b64url_decode(p))
            sig = _b64url_decode(s)
            if not isinstance(self._public, Ed25519PublicKey):
                raise TypeError("invalid public key type")
            self._public.verify(sig, signing_input)
            if int(payload.get("exp", 0)) < int(time.time()):
                raise ValueError("token expired")
            return NodePrincipal(node_id=str(payload.get("sub", "")), is_admin=bool(payload.get("admin", False)))
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=401, detail="invalid token") from exc


jwt_manager = JWTManager()


async def get_current_node(authorization: str = Header(default="")) -> NodePrincipal:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]
    return jwt_manager.verify(token)


async def get_admin_node(node: NodePrincipal = Depends(get_current_node)) -> NodePrincipal:
    if not node.is_admin:
        raise HTTPException(status_code=403, detail="admin role required")
    return node
