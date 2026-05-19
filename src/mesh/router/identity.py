from __future__ import annotations

import duckdb
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption


class NodeIdentity:
    def __init__(self) -> None:
        self._private = ed25519.Ed25519PrivateKey.generate()
        self._public = self._private.public_key()

    def private_key_bytes(self) -> bytes:
        return self._private.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())

    def public_key_bytes(self) -> bytes:
        return self._public.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)


class EIDRegistry:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS eid_registry (node_id VARCHAR PRIMARY KEY, eid VARCHAR, public_key_pem VARCHAR)"
        )

    def upsert(self, node_id: str, eid: str, public_key_pem: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO eid_registry (node_id, eid, public_key_pem) VALUES (?, ?, ?)",
            [node_id, eid, public_key_pem],
        )

    def get(self, node_id: str) -> tuple[str, str] | None:
        row = self.conn.execute(
            "SELECT eid, public_key_pem FROM eid_registry WHERE node_id = ?", [node_id]
        ).fetchone()
        if row is None:
            return None
        return str(row[0]), str(row[1])
