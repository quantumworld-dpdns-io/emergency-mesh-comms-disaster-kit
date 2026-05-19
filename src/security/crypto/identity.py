from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat


@dataclass(slots=True)
class NodeIdentity:
    private_key_pem: bytes
    public_key_pem: bytes


class IdentityManager:
    @staticmethod
    def generate() -> NodeIdentity:
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return NodeIdentity(
            private_key_pem=private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()),
            public_key_pem=public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo),
        )
