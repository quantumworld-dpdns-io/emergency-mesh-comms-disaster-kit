from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import x25519


@dataclass(slots=True)
class HybridKemBundle:
    x25519_public: bytes
    kyber_stub_public: bytes


class HybridKEM:
    def __init__(self) -> None:
        self._x25519_private = x25519.X25519PrivateKey.generate()
        self._kyber_stub_private = b"kyber-768-stub-private"

    def public_bundle(self) -> HybridKemBundle:
        return HybridKemBundle(
            x25519_public=self._x25519_private.public_key().public_bytes_raw(),
            kyber_stub_public=b"kyber-768-stub-public",
        )

    def encapsulate(self, peer: HybridKemBundle) -> bytes:
        peer_x = x25519.X25519PublicKey.from_public_bytes(peer.x25519_public)
        return self._x25519_private.exchange(peer_x) + b"|" + peer.kyber_stub_public
