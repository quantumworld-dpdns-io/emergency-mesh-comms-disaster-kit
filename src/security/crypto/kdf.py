from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int = 32) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=length, salt=salt, info=info).derive(ikm)


def labeled_extract(label: str, ikm: bytes, salt: bytes = b"") -> bytes:
    return hkdf_sha256(ikm=ikm, salt=salt, info=label.encode("utf-8"), length=32)
