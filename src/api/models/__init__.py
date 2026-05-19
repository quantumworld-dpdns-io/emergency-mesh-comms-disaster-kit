from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class BundleRequest(BaseModel):
    destination_eid: str
    payload: str
    priority: str = Field(default="general", pattern="^(emergency|medical|general)$")


class BundleResponse(BaseModel):
    bundle_id: str
    status: str


class NeighborResponse(BaseModel):
    node_id: str
    eid: str
    lqi: float


class MessageRequest(BaseModel):
    to_eid: str
    text: str = Field(max_length=5000)
    priority: str = Field(default="general", pattern="^(emergency|medical|general)$")


class MessageResponse(BaseModel):
    message_id: str
    bundle_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
