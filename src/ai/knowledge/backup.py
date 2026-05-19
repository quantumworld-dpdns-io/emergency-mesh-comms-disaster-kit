from __future__ import annotations

import json
from pathlib import Path

from .qdrant_client import EmergencyQdrantClient


class QdrantBackup:
    def __init__(self, qdrant: EmergencyQdrantClient) -> None:
        self.qdrant = qdrant

    def export_snapshot(self, path: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.qdrant.export_snapshot(), indent=2), encoding="utf-8")

    def restore_snapshot(self, path: str) -> None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.qdrant.restore_snapshot(data)
