from __future__ import annotations

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AesGcmCipher:
    def __init__(self, key: bytes) -> None:
        if len(key) != 32:
            raise ValueError("AES-256-GCM key must be 32 bytes")
        self._key = key

    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes]:
        nonce = os.urandom(12)
        ciphertext = AESGCM(self._key).encrypt(nonce, plaintext, associated_data)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes, associated_data: bytes = b"") -> bytes:
        return AESGCM(self._key).decrypt(nonce, ciphertext, associated_data)
