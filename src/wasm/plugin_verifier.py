from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def sign_wasm(wasm_path: str, private_key_pem: bytes) -> bytes:
    private_key = load_pem_private_key(private_key_pem, password=None)
    if not isinstance(private_key, ed25519.Ed25519PrivateKey):
        raise TypeError("expected Ed25519 private key")
    payload = Path(wasm_path).read_bytes()
    return private_key.sign(payload)


def verify_wasm_signature(wasm_path: str, signature_path: str, public_key_pem: bytes) -> bool:
    public_key = load_pem_public_key(public_key_pem)
    if not isinstance(public_key, ed25519.Ed25519PublicKey):
        raise TypeError("expected Ed25519 public key")
    payload = Path(wasm_path).read_bytes()
    sig = Path(signature_path).read_bytes()
    try:
        public_key.verify(sig, payload)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(payload)
        _ = digest.finalize()
        return True
    except Exception:
        return False
