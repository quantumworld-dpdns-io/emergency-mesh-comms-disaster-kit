from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class Priority(str, Enum):
    emergency = "emergency"
    medical = "medical"
    general = "general"


class EID(BaseModel):
    value: str = Field(min_length=3, max_length=128)


class PrimaryBlock(BaseModel):
    source: EID
    destination: EID
    creation_ts: datetime = Field(default_factory=lambda: datetime.now(UTC))
    ttl_seconds: int = Field(default=3600, ge=1)
    priority: Priority = Priority.general


class Bundle(BaseModel):
    bundle_id: str = Field(default_factory=lambda: str(uuid4()))
    primary: PrimaryBlock
    payload: bytes
    hops: list[str] = Field(default_factory=list)
