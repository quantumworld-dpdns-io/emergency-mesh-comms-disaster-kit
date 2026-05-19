from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from .kdf import hkdf_sha256


@dataclass(slots=True)
class X3DHKeyBundle:
    identity_public: bytes
    signed_prekey_public: bytes
    one_time_prekey_public: bytes


class X3DHParticipant:
    def __init__(self) -> None:
        self.identity_priv = x25519.X25519PrivateKey.generate()
        self.signed_prekey_priv = x25519.X25519PrivateKey.generate()
        self.one_time_prekey_priv = x25519.X25519PrivateKey.generate()

    def public_bundle(self) -> X3DHKeyBundle:
        return X3DHKeyBundle(
            identity_public=self.identity_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw),
            signed_prekey_public=self.signed_prekey_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw),
            one_time_prekey_public=self.one_time_prekey_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw),
        )

    def derive_shared_secret(self, peer_bundle: X3DHKeyBundle) -> bytes:
        peer_id = x25519.X25519PublicKey.from_public_bytes(peer_bundle.identity_public)
        peer_spk = x25519.X25519PublicKey.from_public_bytes(peer_bundle.signed_prekey_public)
        dh1 = self.identity_priv.exchange(peer_spk)
        dh2 = self.signed_prekey_priv.exchange(peer_id)
        dh3 = self.one_time_prekey_priv.exchange(peer_spk)
        return hkdf_sha256(ikm=dh1 + dh2 + dh3, salt=b"x3dh", info=b"emergency-mesh", length=32)
