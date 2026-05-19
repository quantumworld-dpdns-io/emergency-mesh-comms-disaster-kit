from __future__ import annotations

from src.security.crypto.double_ratchet import DoubleRatchet
from src.security.crypto.identity import IdentityManager
from src.security.crypto.replay import ReplayProtector
from src.security.crypto.signing import BundleSigner, BundleVerifier
from src.security.crypto.symmetric import AesGcmCipher
from src.security.crypto.utils import constant_time_eq
from src.security.crypto.x3dh import X3DHParticipant
from src.security.crypto.zkp import SchnorrZKP


def test_sign_verify_round_trip() -> None:
    identity = IdentityManager.generate()
    signer = BundleSigner(identity.private_key_pem)
    verifier = BundleVerifier(identity.public_key_pem)
    payload = b"bundle-payload"
    sig = signer.sign(payload)
    assert verifier.verify(payload, sig)
    assert not verifier.verify(payload + b"x", sig)


def test_x3dh_shared_secret_length() -> None:
    alice = X3DHParticipant()
    bob = X3DHParticipant()
    shared = alice.derive_shared_secret(bob.public_bundle())
    assert len(shared) == 32


def test_double_ratchet_message_keys_change() -> None:
    ratchet = DoubleRatchet(shared_secret=b"s" * 32)
    k1 = ratchet.next_send_message_key()
    k2 = ratchet.next_send_message_key()
    assert k1 != k2


def test_aes_gcm_encrypt_decrypt() -> None:
    cipher = AesGcmCipher(key=b"k" * 32)
    nonce, ct = cipher.encrypt(b"hello", associated_data=b"aad")
    pt = cipher.decrypt(nonce, ct, associated_data=b"aad")
    assert pt == b"hello"


def test_replay_protection() -> None:
    guard = ReplayProtector(window_seconds=120)
    ts = 1_700_000_000.0
    # force an in-window timestamp relative to now by overwriting with runtime value
    import time

    ts = time.time()
    assert not guard.is_replay("nonce-1", ts)
    assert guard.is_replay("nonce-1", ts)


def test_constant_time_eq() -> None:
    assert constant_time_eq(b"abc", b"abc")
    assert not constant_time_eq(b"abc", b"abd")


def test_schnorr_proof_verify() -> None:
    prover = SchnorrZKP()
    proof = prover.prove()
    assert SchnorrZKP.verify(prover.public, proof)
