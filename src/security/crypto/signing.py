from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


class BundleSigner:
    def __init__(self, private_key_pem: bytes) -> None:
        self._private = load_pem_private_key(private_key_pem, password=None)

    def sign(self, payload: bytes) -> bytes:
        if not isinstance(self._private, ed25519.Ed25519PrivateKey):
            raise TypeError("expected ed25519 private key")
        return self._private.sign(payload)


class BundleVerifier:
    def __init__(self, public_key_pem: bytes) -> None:
        self._public = load_pem_public_key(public_key_pem)

    def verify(self, payload: bytes, signature: bytes) -> bool:
        if not isinstance(self._public, ed25519.Ed25519PublicKey):
            raise TypeError("expected ed25519 public key")
        try:
            self._public.verify(signature, payload)
            return True
        except Exception:  # noqa: BLE001
            return False
