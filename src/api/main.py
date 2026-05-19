from __future__ import annotations

from contextlib import asynccontextmanager

import duckdb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.data.arrow.flight_server import MeshFlightServer
from src.data.duckdb.schema import initialize_schema
from src.data.health import DataHealth
from src.data.redis.client import MeshRedisClient


def _build_dependencies() -> tuple[MeshRedisClient, duckdb.DuckDBPyConnection, MeshFlightServer]:
    redis_client = MeshRedisClient(settings.redis_url)
    duck_conn = duckdb.connect(settings.duckdb_path)
    flight = MeshFlightServer(settings.arrow_flight_host, settings.arrow_flight_port)
    return redis_client, duck_conn, flight


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client, duck_conn, flight = _build_dependencies()
    await redis_client.connect()
    initialize_schema(duck_conn)

    app.state.redis_client = redis_client
    app.state.duck_conn = duck_conn
    app.state.flight_server = flight
    app.state.data_health = DataHealth(redis_client, duck_conn, flight)
    try:
        yield
    finally:
        await redis_client.close()
        duck_conn.close()


app = FastAPI(title="Emergency Mesh API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    status = await app.state.data_health.check()
    ok = status["redis"]["ok"] and status["duckdb"]["ok"] and status["arrow"]["ok"]
    return {"status": "ready" if ok else "degraded"}


@app.get("/api/v1/status")
async def status() -> dict[str, object]:
    return {"routing_strategy": "epidemic", "store_depth": 0, "battery": "unknown"}


@app.get("/api/v1/data/health")
async def data_health() -> dict[str, object]:
    return await app.state.data_health.check()
