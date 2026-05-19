from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class Certificate:
    subject: str
    issuer: str
    public_key_pem: bytes
    not_before: datetime
    not_after: datetime


def create_self_signed(subject: str, public_key_pem: bytes, valid_days: int = 30) -> Certificate:
    now = datetime.now(UTC)
    return Certificate(
        subject=subject,
        issuer=subject,
        public_key_pem=public_key_pem,
        not_before=now,
        not_after=now + timedelta(days=valid_days),
    )


def pinned_fingerprint(public_key_pem: bytes) -> str:
    import hashlib

    return hashlib.sha256(public_key_pem).hexdigest()
