from __future__ import annotations

from dataclasses import dataclass

from .tetragon import TetragonEvent


@dataclass(slots=True)
class SecurityClassification:
    category: str
    severity: str
    reason: str


def classify_event(event: TetragonEvent) -> SecurityClassification:
    process = event.process.lower()
    meta = {k: str(v).lower() for k, v in event.metadata.items()}

    if "nmap" in process or meta.get("scan") == "true":
        return SecurityClassification("port_scan", "high", "port scanning pattern")
    if meta.get("retry_count", "0").isdigit() and int(meta.get("retry_count", "0")) > 100:
        return SecurityClassification("retry_flood", "high", "excessive retries")
    if meta.get("eid_known") == "false":
        return SecurityClassification("unknown_eid", "medium", "unknown EID source")
    return SecurityClassification("normal", "low", "no suspicious indicator")
