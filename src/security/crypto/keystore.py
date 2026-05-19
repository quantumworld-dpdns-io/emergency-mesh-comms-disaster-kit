from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path


class SecureKeyStore:
    def __init__(self, path: str = ".secrets/keystore.bin") -> None:
        self.path = Path(path)

    @staticmethod
    def _derive_mask(passphrase: str, salt: bytes, length: int) -> bytes:
        out = b""
        counter = 0
        while len(out) < length:
            counter_bytes = counter.to_bytes(4, "big")
            out += hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt + counter_bytes, 100_000, dklen=32)
            counter += 1
        return out[:length]

    def store(self, key_name: str, secret: bytes, passphrase: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        salt = os.urandom(16)
        mask = self._derive_mask(passphrase, salt, len(secret))
        ciphertext = bytes(a ^ b for a, b in zip(secret, mask, strict=True))
        line = f"{key_name}:{base64.b64encode(salt + ciphertext).decode()}\n"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line)

    def load(self, key_name: str, passphrase: str) -> bytes:
        if not self.path.exists():
            raise KeyError(key_name)
        for line in self.path.read_text(encoding="utf-8").splitlines():
            name, encoded = line.split(":", 1)
            if name != key_name:
                continue
            raw = base64.b64decode(encoded)
            salt, ciphertext = raw[:16], raw[16:]
            mask = self._derive_mask(passphrase, salt, len(ciphertext))
            return bytes(a ^ b for a, b in zip(ciphertext, mask, strict=True))
        raise KeyError(key_name)
