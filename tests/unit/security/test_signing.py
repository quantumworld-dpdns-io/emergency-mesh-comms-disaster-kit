from src.security.crypto.identity import IdentityManager
from src.security.crypto.signing import BundleSigner, BundleVerifier


def test_sign_verify_tamper() -> None:
    ident = IdentityManager.generate()
    s = BundleSigner(ident.private_key_pem)
    v = BundleVerifier(ident.public_key_pem)
    payload = b"abc"
    sig = s.sign(payload)
    assert v.verify(payload, sig)
    assert not v.verify(payload + b"x", sig)
