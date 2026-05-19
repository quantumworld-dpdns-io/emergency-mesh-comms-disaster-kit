from __future__ import annotations


class ReedSolomonFec:
    """Placeholder API compatible with RS(255,223) style usage."""

    def __init__(self, n: int = 255, k: int = 223) -> None:
        self.n = n
        self.k = k

    def encode(self, payload: bytes) -> bytes:
        parity_len = max(self.n - self.k, 0)
        parity = bytes([sum(payload) % 256]) * min(parity_len, 32)
        return payload + parity

    def decode(self, payload_with_parity: bytes) -> bytes:
        parity_len = min(max(self.n - self.k, 0), 32)
        if parity_len == 0:
            return payload_with_parity
        return payload_with_parity[:-parity_len]
