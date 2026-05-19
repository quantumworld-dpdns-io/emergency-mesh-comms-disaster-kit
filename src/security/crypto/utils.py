from __future__ import annotations

import hmac


def constant_time_eq(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
