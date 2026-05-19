# emergency-mesh-comms-disaster-kit

Production-grade emergency mesh communications kit that turns phones and LoRa devices into resilient DTN-inspired message meshes during outages.

## Architecture

- `src/mesh`: Bundle Protocol v7 models, routing, store-and-forward, transport manager.
- `src/lora`: LoRa drivers, packet codecs, ADR/FHSS/ARQ.
- `src/api`: FastAPI REST + WebSocket + auth + audit endpoint.
- `src/ai`: Ollama/LangGraph-style coordinator, MCP, RAG, federated learning.
- `src/data`: Redis, DuckDB analytics, Arrow IPC/Flight.
- `src/wasm`: Rust WASM plugins + Wasmtime host runtime.
- `src/web`: React/TypeScript PWA, offline queue, websocket updates.

## Quickstart

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
make dev
```

## Full Stack (Docker)

```bash
docker compose -f docker/docker-compose.yml up -d
```

Services:
- API: `http://localhost:8080`
- Web: `http://localhost:8081`
- Qdrant: `http://localhost:6333`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Phoenix: `http://localhost:6006`

## Raspberry Pi / LoRa Notes

- Set `LORA_ENABLED=true` and choose `LORA_DRIVER=sx127x` or `rfm95w`.
- Configure `LORA_PORT` and regional band (`US915` / `EU868`) in `.env`.
- Validate duty cycle and ADR settings before live deployment.

## Runbooks and Plans

- Disaster deployment runbook: `docs/runbooks/disaster-deployment.md`
- Comprehensive implementation roadmap: `docs/plans/claude_plan.md`

## Testing

```bash
make test
pytest tests/integration -q
robot tests/robot/functional
robot tests/robot/security
```

## License

MIT
