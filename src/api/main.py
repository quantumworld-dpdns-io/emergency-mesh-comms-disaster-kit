from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from uuid import uuid4

import duckdb
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.auth.api_key import require_api_key
from src.api.auth.jwt import NodePrincipal, get_admin_node, get_current_node, jwt_manager
from src.api.models import (
    BundleRequest,
    BundleResponse,
    MessageRequest,
    MessageResponse,
    NeighborResponse,
    ProblemDetails,
)
from src.config import settings
from src.data.arrow.flight_server import MeshFlightServer
from src.data.duckdb.schema import initialize_schema
from src.data.health import DataHealth
from src.data.redis.client import MeshRedisClient


class InMemoryStore:
    def __init__(self) -> None:
        self.bundles: dict[str, dict[str, object]] = {}
        self.messages: list[dict[str, object]] = []
        self.neighbors: list[NeighborResponse] = [
            NeighborResponse(node_id="node-2", eid="dtn://node-2", lqi=72.5),
            NeighborResponse(node_id="node-3", eid="dtn://node-3", lqi=63.2),
        ]
        self.events: asyncio.Queue[dict[str, object]] = asyncio.Queue()


def _build_dependencies() -> tuple[MeshRedisClient | None, duckdb.DuckDBPyConnection, MeshFlightServer]:
    duck_conn = duckdb.connect(settings.duckdb_path)
    flight = MeshFlightServer(settings.arrow_flight_host, settings.arrow_flight_port)
    try:
        redis_client = MeshRedisClient(settings.redis_url)
        return redis_client, duck_conn, flight
    except Exception:  # noqa: BLE001
        return None, duck_conn, flight


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client, duck_conn, flight = _build_dependencies()
    if redis_client is not None:
        try:
            await redis_client.connect()
        except Exception:  # noqa: BLE001
            redis_client = None

    initialize_schema(duck_conn)

    app.state.redis_client = redis_client
    app.state.duck_conn = duck_conn
    app.state.flight_server = flight
    app.state.data_health = DataHealth(redis_client, duck_conn, flight) if redis_client else None
    app.state.mem = InMemoryStore()
    try:
        yield
    finally:
        if redis_client is not None:
            await redis_client.close()
        duck_conn.close()


app = FastAPI(
    title="Emergency Mesh API",
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "bundles", "description": "Bundle operations"},
        {"name": "messages", "description": "Messaging operations"},
        {"name": "network", "description": "Topology and neighbors"},
        {"name": "admin", "description": "Emergency and privileged operations"},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_guard_middleware(request: Request, call_next):
    raw = await request.body()
    if len(raw) > 1024 * 1024:
        raise HTTPException(status_code=413, detail="request body too large")
    if b"\x00" in raw:
        raise HTTPException(status_code=400, detail="null byte not allowed")
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


@app.exception_handler(HTTPException)
async def http_problem_handler(request: Request, exc: HTTPException):
    problem = ProblemDetails(
        type="about:blank",
        title="HTTP Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=str(request.url.path),
    )
    return JSONResponse(status_code=exc.status_code, content=problem.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_problem_handler(request: Request, exc: RequestValidationError):
    problem = ProblemDetails(
        type="https://example.com/problems/validation-error",
        title="Validation Error",
        status=422,
        detail=str(exc.errors()),
        instance=str(request.url.path),
    )
    return JSONResponse(status_code=422, content=problem.model_dump())


@app.exception_handler(Exception)
async def unhandled_problem_handler(request: Request, exc: Exception):
    problem = ProblemDetails(
        type="https://example.com/problems/internal-error",
        title="Internal Server Error",
        status=500,
        detail=str(exc),
        instance=str(request.url.path),
    )
    return JSONResponse(status_code=500, content=problem.model_dump())


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/api/v1/auth/token")
async def issue_token(node_id: str, admin: bool = False) -> dict[str, str]:
    return {"token": jwt_manager.issue(node_id=node_id, is_admin=admin)}


@app.post(
    "/api/v1/bundles",
    response_model=BundleResponse,
    tags=["bundles"],
    openapi_extra={"examples": [{"destination_eid": "dtn://node-2", "payload": "ping", "priority": "general"}]},
)
async def submit_bundle(
    req: BundleRequest,
    _node: NodePrincipal = Depends(get_current_node),
) -> BundleResponse:
    bundle_id = str(uuid4())
    app.state.mem.bundles[bundle_id] = {
        "status": "queued",
        "destination": req.destination_eid,
        "payload": req.payload,
        "priority": req.priority,
        "hops": 0,
        "created_at": datetime.now(UTC).isoformat(),
    }
    await app.state.mem.events.put({"type": "bundle_queued", "bundle_id": bundle_id})
    return BundleResponse(bundle_id=bundle_id, status="queued")


@app.get("/api/v1/bundles/{bundle_id}", tags=["bundles"])
async def bundle_status(bundle_id: str, _node: NodePrincipal = Depends(get_current_node)) -> dict[str, object]:
    item = app.state.mem.bundles.get(bundle_id)
    if item is None:
        raise HTTPException(status_code=404, detail="bundle not found")
    return {"bundle_id": bundle_id, "status": item["status"], "hops": item["hops"]}


@app.get("/api/v1/neighbors", response_model=list[NeighborResponse], tags=["network"])
async def neighbors(_node: NodePrincipal = Depends(get_current_node)) -> list[NeighborResponse]:
    return app.state.mem.neighbors


@app.get("/api/v1/status", tags=["network"])
async def status(_node: NodePrincipal = Depends(get_current_node)) -> dict[str, object]:
    return {"routing_strategy": "epidemic", "store_depth": len(app.state.mem.bundles), "battery": "unknown"}


@app.post("/api/v1/messages", response_model=MessageResponse, tags=["messages"])
async def send_message(
    req: MessageRequest,
    _client: str = Depends(require_api_key),
    _node: NodePrincipal = Depends(get_current_node),
) -> MessageResponse:
    bundle_id = str(uuid4())
    message_id = str(uuid4())
    app.state.mem.bundles[bundle_id] = {
        "status": "queued",
        "destination": req.to_eid,
        "payload": req.text,
        "priority": req.priority,
        "hops": 0,
    }
    app.state.mem.messages.append(
        {
            "message_id": message_id,
            "bundle_id": bundle_id,
            "to_eid": req.to_eid,
            "text": req.text,
            "priority": req.priority,
            "created_at": datetime.now(UTC).isoformat(),
        }
    )
    await app.state.mem.events.put({"type": "message_sent", "message_id": message_id, "bundle_id": bundle_id})
    return MessageResponse(message_id=message_id, bundle_id=bundle_id)


@app.get("/api/v1/messages", tags=["messages"])
async def inbox(limit: int = 50, cursor: int = 0, _node: NodePrincipal = Depends(get_current_node)) -> dict[str, object]:
    messages = app.state.mem.messages[cursor : cursor + limit]
    next_cursor = cursor + len(messages)
    if next_cursor >= len(app.state.mem.messages):
        next_cursor = -1
    return {"items": messages, "next_cursor": next_cursor}


@app.post("/api/v1/emergency", tags=["admin"])
async def emergency_broadcast(
    message: str,
    _admin: NodePrincipal = Depends(get_admin_node),
) -> dict[str, object]:
    event = {"type": "emergency", "message": message, "neighbors": len(app.state.mem.neighbors)}
    await app.state.mem.events.put(event)
    return {"status": "broadcasted", "targets": len(app.state.mem.neighbors)}


@app.get("/api/v1/topology", tags=["network"])
async def topology(_node: NodePrincipal = Depends(get_current_node)) -> dict[str, object]:
    nodes = [{"id": "node-1"}] + [{"id": n.node_id} for n in app.state.mem.neighbors]
    edges = [{"from": "node-1", "to": n.node_id, "lqi": n.lqi} for n in app.state.mem.neighbors]
    return {"nodes": nodes, "edges": edges}


@app.get("/api/v1/analytics", tags=["network"])
async def analytics(_node: NodePrincipal = Depends(get_current_node)) -> dict[str, float]:
    queued = len(app.state.mem.bundles)
    delivered = sum(1 for v in app.state.mem.bundles.values() if v["status"] == "delivered")
    ratio = 0.0 if queued == 0 else delivered / queued
    return {"delivery_ratio": ratio, "throughput": float(queued), "latency_ms_p95": 0.0}


@app.websocket("/api/v1/ws")
async def websocket_updates(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            event = await app.state.mem.events.get()
            await ws.send_text(json.dumps(event))
    except WebSocketDisconnect:
        return


@app.get("/api/v1/data/health")
async def data_health() -> dict[str, object]:
    if app.state.data_health is None:
        return {"redis": {"ok": False}, "duckdb": {"ok": True}, "arrow": {"ok": True}}
    return await app.state.data_health.check()
