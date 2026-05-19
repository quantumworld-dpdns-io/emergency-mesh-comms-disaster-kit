# emergency-mesh-comms-disaster-kit

Production-oriented emergency mesh communications kit for disaster conditions.

## Architecture

- DTN-inspired store-and-forward mesh router
- Multi-transport adapters (UDP/TCP/LoRa/WiFi Direct/BT/SMS)
- FastAPI control/data plane
- Offline-first React PWA client
- Redis + DuckDB + Arrow + Qdrant data stack
- Optional AI coordination with Ollama/LangGraph/CrewAI

## Quickstart

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
make dev
```

## Project Layout

- `src/mesh`: protocol, routing, transport
- `src/lora`: LoRa drivers and packet pipeline
- `src/data`: Redis/DuckDB/Arrow integration
- `src/security`: crypto + audit
- `src/api`: FastAPI API
- `src/ai`: AI coordinator, RAG, MCP, federated
- `src/wasm`: WASM plugins and host runtime
- `src/web`: PWA client

## Runbook

Operational runbook: `docs/runbooks/disaster-deployment.md`

## License

MIT
