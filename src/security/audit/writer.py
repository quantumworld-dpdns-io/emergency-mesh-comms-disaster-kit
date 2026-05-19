from __future__ import annotations

from datetime import UTC, datetime

from .integrity import AuditIntegrityChain


class AuditLogWriter:
    def __init__(self, redis_client=None, duck_conn=None) -> None:
        self.redis_client = redis_client
        self.duck_conn = duck_conn
        self.integrity = AuditIntegrityChain()
        self._memory: list[dict[str, object]] = []

    def records(self) -> list[dict[str, object]]:
        return list(self._memory)

    async def write(self, event: dict[str, object]) -> dict[str, object]:
        enriched = {
            **event,
            "ts": event.get("ts") or datetime.now(UTC).isoformat(),
        }
        chained = self.integrity.append(enriched)
        out = {**enriched, "prev_hash": chained.prev_hash, "hash": chained.hash}
        self._memory.append(out)

        if self.redis_client is not None:
            try:
                await self.redis_client.client.xadd("mesh:audit:security", out)
            except Exception:
                pass

        if self.duck_conn is not None:
            try:
                self.duck_conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS security_audit_events (
                        ts TIMESTAMP,
                        category VARCHAR,
                        severity VARCHAR,
                        process VARCHAR,
                        detail VARCHAR,
                        event_hash VARCHAR,
                        prev_hash VARCHAR
                    )
                    """
                )
                self.duck_conn.execute(
                    "INSERT INTO security_audit_events VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [
                        out.get("ts"),
                        out.get("category", "unknown"),
                        out.get("severity", "low"),
                        out.get("process", ""),
                        str(out.get("detail", "")),
                        out.get("hash"),
                        out.get("prev_hash"),
                    ],
                )
            except Exception:
                pass

        return out
