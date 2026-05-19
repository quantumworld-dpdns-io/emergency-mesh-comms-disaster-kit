Emergency Mesh Comms Disaster Kit — Comprehensive Implementation Plan

 Context

 Project: emergency-mesh-comms-disaster-kit
 Current State: Greenfield scaffold — empty src/, empty tests/, placeholder CI, 1 commit
 Goal: Build a production-grade emergency mesh communications kit that turns phones and LoRa devices into resilient DTN-inspired message meshes during network outages
 Integration: Tools from /Users/dennis_leedennis_lee/Documents/GitHub/academy-central/software-tools/

 ▎ Note: The user specified /Users/dennis_leedennis_lee/Desktop/software-tools — this path does not exist. The actual tools directory is at
 ▎ /Users/dennis_leedennis_lee/Documents/GitHub/academy-central/software-tools/.

 ---
 Architecture

 src/
 ├── mesh/           # DTN mesh routing engine (Python + Go gRPC)
 │   ├── protocol/   # Bundle Protocol v7 (CBOR), fragmentation, custody
 │   ├── router/     # Epidemic/PRoPHET/SprayWait, store-and-forward, Go forwarder
 │   └── transport/  # UDP, TCP, WiFi Direct, BT, SMS, LoRa, WASM adapters
 ├── lora/           # LoRa hardware (SX127x, RFM95W), ARQ, CSMA/CA, FHSS
 ├── ai/             # LangGraph coordinator + CrewAI crew + Ollama + Qdrant RAG + MCP
 ├── api/            # FastAPI REST + WebSocket + JWT auth
 ├── web/            # React/TypeScript PWA (offline-first, service worker)
 ├── data/           # Redis, DuckDB, Apache Arrow Flight
 ├── security/       # E2E crypto (X3DH + Double Ratchet), Tetragon audit
 └── wasm/           # Rust WASM plugins (routing, compression, CRC) via Wasmtime

 tests/
 ├── unit/           # pytest (255 tests across all modules)
 ├── integration/    # pytest with testcontainers (Redis, Qdrant)
 ├── robot/
 │   ├── functional/ # Robot Framework acceptance tests
 │   ├── e2e/        # Full disaster scenario + PWA Playwright tests
 │   └── security/   # OWASP Top 10 (A01–A10) + ZAP active scan
 └── performance/    # Locust load tests

 .github/workflows/
 ├── ci.yml          # lint + unit + integration (blocks merge)
 ├── security.yml    # pip-audit, bandit, semgrep, trivy, ZAP
 ├── robot-tests.yml # Robot Framework functional + OWASP security
 ├── performance.yml # Locust headless, p95 assertion
 ├── wasm-build.yml  # Rust WASM compile + ed25519 sign
 ├── docker.yml      # Build + push to GHCR
 └── deploy.yml      # SSH deploy + health gate + rollback

 Key tech integrations from software-tools:
 - Wasmtime → sandboxed transport plugins (src/wasm/)
 - Ollama / llama.cpp → offline AI inference (src/ai/models/)
 - LangGraph + CrewAI → stateful mesh coordinator + disaster response crew (src/ai/agents/)
 - Model Context Protocol → MCP server exposing mesh tools to AI agents (src/ai/mcp/)
 - Redis → pub/sub, geo index, rate limiting, audit stream, leader election
 - Qdrant → RAG knowledge base for emergency procedures
 - DuckDB → embedded analytics, ETL from Redis streams
 - Apache Arrow → Flight server for bulk data export, zero-copy interchange
 - Cilium Tetragon → eBPF runtime security, syscall-level audit
 - Arize Phoenix → local LLM observability (no cloud dependency)
 - Flower → federated learning for routing model across mesh nodes

 ---
 Phase Overview

 ┌───────┬───────────────────────────────────────┬─────────┐
 │ Phase │                 Name                  │ Commits │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 1     │ Foundation & Project Skeleton         │ 1–20    │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 2     │ Core DTN Mesh Router (Python)         │ 21–45   │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 3     │ Mesh Transport Adapters               │ 46–65   │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 4     │ LoRa Hardware Integration             │ 66–85   │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 5     │ Data Layer (Redis, DuckDB, Arrow)     │ 86–105  │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 6     │ Cryptography & E2E Security           │ 106–120 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 7     │ FastAPI REST Layer                    │ 121–140 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 8     │ WebAssembly Modules (Wasmtime)        │ 141–155 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 9     │ AI Agents (Ollama, LangGraph, CrewAI) │ 156–180 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 10    │ MCP Server & Qdrant RAG               │ 181–195 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 11    │ Phone PWA (React/TypeScript)          │ 196–220 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 12    │ Cilium Tetragon & Audit Layer         │ 221–230 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 13    │ Federated Learning (Flower)           │ 231–240 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 14    │ Unit Tests (pytest)                   │ 241–255 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 15    │ Robot Framework — Functional & E2E    │ 256–270 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 16    │ Robot Framework — OWASP Top 10        │ 271–285 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 17    │ CI/CD Pipelines (GitHub Actions)      │ 286–295 │
 ├───────┼───────────────────────────────────────┼─────────┤
 │ 18    │ Docker, Observability & Docs          │ 296–300 │
 └───────┴───────────────────────────────────────┴─────────┘

 ---
 300 Todos (1 commit each)

 Phase 1 — Foundation & Project Skeleton (1–20)

 - [1] chore: initialize Python project with pyproject.toml — pyproject.toml with ruff/pytest/mypy config, Python 3.12
 - [2] chore: add root requirements files for all layers — requirements.txt, requirements-dev.txt, requirements-ai.txt, requirements-lora.txt
 - [3] chore: expand .gitignore for full Python/Go/Node stack — adds *.wasm, go/, coverage/, .mypy_cache/, htmlcov/
 - [4] chore: initialize Go module for mesh router — src/mesh/go.mod, go.sum placeholder; Go 1.22
 - [5] chore: scaffold all src/ subdirectory __init__.py files — init.py in mesh/, lora/, ai/, api/, data/, security/
 - [6] chore: scaffold tests/ directory structure with markers — tests/init.py, unit/, integration/, performance/; pytest.ini
 - [7] chore: add pre-commit configuration — .pre-commit-config.yaml with ruff, mypy, gofmt, hadolint, detect-secrets
 - [8] docs: add ADR-001 for DTN mesh architecture decision — docs/architecture/ADR-001-dtn-mesh-approach.md
 - [9] docs: add ADR-002 for AI agent stack selection — docs/architecture/ADR-002-ai-agent-stack.md
 - [10] docs: add ADR-003 for transport adapter abstraction — docs/architecture/ADR-003-transport-adapters.md
 - [11] docs: add ADR-004 for WebAssembly sandbox strategy — docs/architecture/ADR-004-wasm-sandboxing.md
 - [12] docs: add system architecture overview diagram source — docs/architecture/system-overview.md with ASCII block diagram
 - [13] docs: add OpenAPI spec skeleton for REST API — docs/api/openapi.yaml with OpenAPI 3.1.0 header
 - [14] docs: add operational runbook for disaster deployment — docs/runbooks/disaster-deployment.md
 - [15] chore: add .env.example with all required variables — REDIS_URL, QDRANT_URL, OLLAMA_URL, LORA_PORT, SECRET_KEY, etc.
 - [16] chore: add Makefile with dev workflow targets — make dev, test, lint, build-wasm, robot, security-scan, docker-up
 - [17] chore: configure ruff with comprehensive rule set — rules E,W,F,I,N,UP,S,B,A,C4,PT,RUF; line-length=100
 - [18] chore: configure mypy with strict mode — strict=true, pydantic plugin, per-module overrides
 - [19] chore: add shared pydantic base settings module — src/config.py with Settings class, env_file=".env"
 - [20] chore: add shared logging configuration module — src/logging_config.py with structlog, JSON output, OTel trace-id

 Phase 2 — Core DTN Mesh Router (21–45)

 - [21] feat(mesh): define Bundle Protocol v7 data structures — src/mesh/protocol/bundle.py with Bundle, PrimaryBlock, EID pydantic models
 - [22] feat(mesh): implement bundle serialization with CBOR — src/mesh/protocol/serializer.py using cbor2
 - [23] feat(mesh): define fragment and reassembly types — src/mesh/protocol/fragmentation.py with Fragment, ReassemblyBuffer
 - [24] feat(mesh): implement custody transfer signaling — src/mesh/protocol/custody.py with CustodySignal, RetransmissionPolicy
 - [25] feat(mesh): define routing table and neighbor model — src/mesh/router/routing_table.py with Neighbor, RoutingEntry, TTL eviction
 - [26] feat(mesh): implement epidemic routing algorithm — src/mesh/router/epidemic.py with EpidemicRouter, summary vector comparison
 - [27] feat(mesh): implement PRoPHET routing algorithm — src/mesh/router/prophet.py with delivery predictability matrix, aging
 - [28] feat(mesh): implement spray-and-wait routing — src/mesh/router/spray_wait.py with binary spray phase, L token counter
 - [29] feat(mesh): add router factory and strategy selector — src/mesh/router/factory.py with RouterFactory.create()
 - [30] feat(mesh): implement store-and-forward bundle queue — src/mesh/router/bundle_store.py with aiosqlite backend
 - [31] feat(mesh): add bundle TTL expiration worker — src/mesh/router/expiry_worker.py asyncio task, 30s polling
 - [32] feat(mesh): implement contact graph with link estimation — src/mesh/router/contact_graph.py with RSSI/duration edge weights
 - [33] feat(mesh): add CGR (Contact Graph Routing) stub — src/mesh/router/cgr.py Dijkstra over ContactGraph
 - [34] feat(mesh): implement neighbor discovery beacon — src/mesh/router/beacon.py UDP multicast 224.0.0.251:4554
 - [35] feat(mesh): add Go mesh core — bundle forwarding engine — src/mesh/router/forwarder.go goroutine pipeline
 - [36] feat(mesh): add Go mesh core — neighbor table — src/mesh/router/neighbor_table.go sync.RWMutex thread-safe
 - [37] feat(mesh): add Go mesh core — metrics exporter — src/mesh/router/metrics.go Prometheus counters
 - [38] feat(mesh): add Go mesh core — gRPC service definition — src/mesh/protocol/mesh.proto with MeshService RPCs
 - [39] feat(mesh): implement gRPC server in Go — src/mesh/router/grpc_server.go implementing MeshServiceServer
 - [40] feat(mesh): add Python gRPC client for mesh router — src/mesh/router/client.py with MeshRouterClient async methods
 - [41] feat(mesh): implement link-state advertisement flooding — src/mesh/router/lsa.py with LSAManager, sequence numbers
 - [42] feat(mesh): add multipath bundle scheduling — src/mesh/router/scheduler.py priority queue (emergency > medical > general)
 - [43] feat(mesh): implement bundle deduplication — src/mesh/router/dedup.py rolling Bloom filter on Redis bitfield
 - [44] feat(mesh): add mesh node identity and EID registry — src/mesh/router/identity.py ed25519 keypair + EIDRegistry in DuckDB
 - [45] feat(mesh): wire mesh router into async application loop — src/mesh/app.py MeshApplication asyncio entrypoint

 Phase 3 — Mesh Transport Adapters (46–65)

 - [46] feat(transport): define abstract transport base class — src/mesh/transport/base.py Transport ABC: send, receive, discover
 - [47] feat(transport): implement UDP LAN transport adapter — src/mesh/transport/udp.py asyncio UDP, MTU fragmentation
 - [48] feat(transport): implement TCP stream transport adapter — src/mesh/transport/tcp.py asyncio StreamReader/Writer, TLS optional
 - [49] feat(transport): implement WiFi Direct transport stub — src/mesh/transport/wifi_direct.py wpa_supplicant DBus
 - [50] feat(transport): implement Bluetooth RFCOMM transport stub — src/mesh/transport/bluetooth.py pybluez2 SDP
 - [51] feat(transport): implement SMS fallback transport — src/mesh/transport/sms.py base64 over gammu/AT+CMGS
 - [52] feat(transport): add transport registry and hot-swap — src/mesh/transport/registry.py dynamic registration, failover
 - [53] feat(transport): implement transport health monitor — src/mesh/transport/health.py 10s ping, Redis pub/sub status
 - [54] feat(transport): add bandwidth estimation module — src/mesh/transport/bandwidth.py EWMA per transport
 - [55] feat(transport): implement transport-level compression — src/mesh/transport/compression.py zstd with dictionary
 - [56] feat(transport): add forward error correction layer — src/mesh/transport/fec.py Reed-Solomon (255,223)
 - [57] feat(transport): implement packet prioritization queue — src/mesh/transport/priority_queue.py 3-tier FIFO
 - [58] feat(transport): add transport statistics collector — src/mesh/transport/stats.py tx/rx bytes, errors, latency
 - [59] feat(transport): implement link quality indicator module — src/mesh/transport/lqi.py RSSI+SNR+PER composite 0-100
 - [60] feat(transport): add mesh topology event bus — src/mesh/transport/event_bus.py Redis pub/sub typed events
 - [61] feat(transport): implement QoS-aware transport selection — src/mesh/transport/qos_selector.py bandwidth × LQI / latency
 - [62] feat(transport): add simulated transport for testing — src/mesh/transport/simulated.py configurable delay/loss/bandwidth
 - [63] feat(transport): implement multicast overlay for mesh — src/mesh/transport/multicast.py IP multicast per cluster
 - [64] feat(transport): add transport plugin loader via Wasmtime — src/mesh/transport/wasm_loader.py Wasmtime Python bindings
 - [65] feat(transport): wire all transports into transport manager — src/mesh/transport/manager.py concurrent receive loops

 Phase 4 — LoRa Hardware Integration (66–85)

 - [66] feat(lora): define LoRa hardware abstraction interface — src/lora/drivers/base.py LoRaDriver ABC
 - [67] feat(lora): implement SX1276/SX1278 driver via spidev — src/lora/drivers/sx127x.py register-level SPI programming
 - [68] feat(lora): implement RFM95W driver (Adafruit CircuitPython) — src/lora/drivers/rfm95w.py adafruit_rfm9x wrapper
 - [69] feat(lora): add LoRa hardware detection and auto-select — src/lora/drivers/detector.py SPI bus probe
 - [70] feat(lora): implement LoRa packet format encoder — src/lora/packets/encoder.py header+payload+CRC-32
 - [71] feat(lora): implement LoRa packet format decoder — src/lora/packets/decoder.py CRC validation, LoRaPacket dataclass
 - [72] feat(lora): define all LoRa packet types and flags — src/lora/packets/types.py PacketType enum, PacketFlags bitmask
 - [73] feat(lora): implement large message segmentation — src/lora/packets/segmentation.py sliding window reassembly
 - [74] feat(lora): add ARQ (Automatic Repeat reQuest) layer — src/lora/packets/arq.py stop-and-wait, configurable retries
 - [75] feat(lora): implement CSMA/CA for LoRa channel access — src/lora/drivers/csma_ca.py CAD before TX, random backoff
 - [76] feat(lora): add frequency hopping spread spectrum support — src/lora/drivers/fhss.py 50-channel hop table, beacon sync
 - [77] feat(lora): implement LoRa transport adapter — src/lora/lora_transport.py extends Transport base
 - [78] feat(lora): add RSSI and SNR telemetry collector — src/lora/telemetry.py time-series in DuckDB lora_telemetry
 - [79] feat(lora): implement LoRa duty cycle limiter — src/lora/drivers/duty_cycle.py 1% EU 868 MHz enforcement
 - [80] feat(lora): add LoRa adaptive data rate controller — src/lora/drivers/adr.py SF/TXPower from SNR history
 - [81] feat(lora): implement LoRa gateway bridge mode — src/lora/gateway.py MQTT to ChirpStack when internet available
 - [82] feat(lora): add LoRa channel scanner — src/lora/scanner.py 915/868 MHz sub-band scan, noise floor
 - [83] feat(lora): implement LoRa mesh transport unit tests — tests/unit/lora/test_encoder_decoder.py round-trip, CRC errors
 - [84] feat(lora): add LoRa simulator for offline testing — src/lora/drivers/simulator.py Gaussian noise, loss model
 - [85] feat(lora): wire LoRa transport into transport manager — auto-register when LORA_ENABLED=true, graceful shutdown

 Phase 5 — Data Layer: Redis, DuckDB, Apache Arrow (86–105)

 - [86] feat(data): implement Redis client wrapper with retry — src/data/redis/client.py MeshRedisClient, exponential backoff
 - [87] feat(data): define Redis key schema and namespaces — src/data/redis/schema.py constants + TTL policies
 - [88] feat(data): implement Redis pub/sub event dispatcher — src/data/redis/pubsub.py typed subscription, asyncio.Queue fan-out
 - [89] feat(data): add Redis geospatial index for node tracking — src/data/redis/geo.py GEOADD/GEORADIUS wrappers
 - [90] feat(data): implement Redis stream for bundle audit log — src/data/redis/audit_stream.py XADD on enqueue/forward/deliver
 - [91] feat(data): implement Redis distributed lock for leader election — src/data/redis/leader_election.py Redlock algorithm
 - [92] feat(data): add Redis rate limiter for API and transport — src/data/redis/rate_limiter.py sliding window sorted-set
 - [93] feat(data): initialize DuckDB schema for mesh analytics — src/data/duckdb/schema.py DDL for 5 analytics tables
 - [94] feat(data): implement DuckDB bundle analytics queries — src/data/duckdb/bundle_analytics.py delivery ratio, latency
 - [95] feat(data): add DuckDB neighbor graph analytics — src/data/duckdb/neighbor_analytics.py contact frequency, uptime
 - [96] feat(data): implement DuckDB ETL from Redis streams — src/data/duckdb/etl.py StreamETL, 60s bulk insert
 - [97] feat(data): add DuckDB parquet export for offline analysis — src/data/duckdb/exporter.py COPY TO parquet
 - [98] feat(data): define Apache Arrow schemas for interchange — src/data/arrow/schemas.py pyarrow.Schema for all records
 - [99] feat(data): implement Arrow IPC reader/writer — src/data/arrow/ipc.py RecordBatchStreamWriter/Reader
 - [100] feat(data): add Arrow Flight server for bulk data export — src/data/arrow/flight_server.py MeshFlightServer
 - [101] feat(data): implement in-memory Arrow table for hot metrics — src/data/arrow/hot_metrics.py ring-buffer 10k events
 - [102] feat(data): add data layer integration tests — tests/integration/data/ with testcontainers Redis + DuckDB fixtures
 - [103] feat(data): implement data retention and purge policy — src/data/retention.py RetentionManager, nightly DuckDB DELETE
 - [104] feat(data): add data layer health endpoints — src/data/health.py Redis ping, DuckDB latency, Arrow reachability
 - [105] feat(data): wire data layer into application startup — initialize all clients in mesh/app.py and api/main.py

 Phase 6 — Cryptography & E2E Security (106–120)

 - [106] feat(crypto): implement node identity key generation — src/security/crypto/identity.py ed25519 keypair, PEM serialization
 - [107] feat(crypto): implement bundle signing and verification — src/security/crypto/signing.py BundleSigner + BundleVerifier
 - [108] feat(crypto): implement X3DH key agreement for E2E — src/security/crypto/x3dh.py identity + signed prekeys
 - [109] feat(crypto): implement Double Ratchet for forward secrecy — src/security/crypto/double_ratchet.py DH + symmetric ratchet
 - [110] feat(crypto): add AES-256-GCM payload encryption — src/security/crypto/symmetric.py random nonce, AD binding
 - [111] feat(crypto): implement key derivation and HKDF utilities — src/security/crypto/kdf.py HKDF-SHA-256 labeled extraction
 - [112] feat(crypto): add public key infrastructure (PKI) stub — src/security/crypto/pki.py self-signed X.509, cert pinning
 - [113] feat(crypto): implement secure key storage with OS keyring — src/security/crypto/keystore.py keyring + PBKDF2 fallback
 - [114] feat(crypto): add post-quantum key encapsulation stub — src/security/crypto/pqc.py liboqs-python Kyber-768, X25519+Kyber hybrid
 - [115] feat(crypto): implement replay attack prevention — src/security/crypto/replay.py nonce/timestamp window in Redis
 - [116] feat(crypto): add bundle encryption integration — wire encryption into bundle.py and forwarder.go
 - [117] feat(crypto): implement certificate rotation scheduler — src/security/crypto/rotation.py 7-day signed prekey rotation
 - [118] feat(crypto): add crypto unit tests — tests/unit/security/ signing, X3DH, double ratchet with Hypothesis
 - [119] feat(crypto): add timing-safe comparison utilities — src/security/crypto/utils.py hmac.compare_digest wrappers
 - [120] feat(crypto): implement zero-knowledge node authentication — src/security/crypto/zkp.py Schnorr proof-of-knowledge

 Phase 7 — FastAPI REST Layer (121–140)

 - [121] feat(api): initialize FastAPI application — src/api/main.py lifespan, CORS, Prometheus, router includes
 - [122] feat(api): add pydantic request/response models — src/api/models/ BundleRequest, NeighborResponse, MessageRequest
 - [123] feat(api): implement bundle submission endpoint — POST /api/v1/bundles with encryption + mesh enqueue
 - [124] feat(api): implement bundle status endpoint — GET /api/v1/bundles/{bundle_id} delivery status + hops
 - [125] feat(api): implement neighbor listing endpoint — GET /api/v1/neighbors with LQI scores
 - [126] feat(api): implement node status endpoint — GET /api/v1/status routing strategy, store depth, battery
 - [127] feat(api): implement message send endpoint — POST /api/v1/messages high-level text API over bundles
 - [128] feat(api): implement message inbox endpoint — GET /api/v1/messages paginated with cursor
 - [129] feat(api): add emergency alert broadcast endpoint — POST /api/v1/emergency admin-only, all-neighbor flood
 - [130] feat(api): implement network topology endpoint — GET /api/v1/topology ContactGraph as JSON graph
 - [131] feat(api): implement analytics dashboard endpoint — GET /api/v1/analytics delivery ratio, throughput, latency
 - [132] feat(api): add JWT authentication middleware — src/api/auth/jwt.py ed25519 JWT, Depends(get_current_node)
 - [133] feat(api): add API key authentication for device clients — src/api/auth/api_key.py hashed keys in Redis, rotation
 - [134] feat(api): implement security headers middleware — HSTS, X-Content-Type-Options, CSP, Permissions-Policy
 - [135] feat(api): add request validation and sanitization middleware — 1MB limit, null byte strip, audit log
 - [136] feat(api): implement WebSocket endpoint for live updates — GET /api/v1/ws MeshEventBus subscriber
 - [137] feat(api): add OpenAPI documentation with examples — openapi_tags, response_model, openapi_extra examples
 - [138] feat(api): implement graceful API error handling — RFC 7807 Problem Details JSON for all error classes
 - [139] feat(api): add health and readiness probe endpoints — GET /healthz (liveness) GET /readyz (readiness)
 - [140] feat(api): add API integration tests with TestClient — tests/integration/api/ bundle, message, auth endpoints

 Phase 8 — WebAssembly Modules via Wasmtime (141–155)

 - [141] feat(wasm): initialize Rust workspace for WASM modules — src/wasm/Cargo.toml workspace, wasm32-wasip2 target
 - [142] feat(wasm): implement routing plugin in Rust (WASM) — src/wasm/routing-plugin/ exports should_forward()
 - [143] feat(wasm): implement compression plugin in Rust (WASM) — src/wasm/compression-plugin/ exports compress/decompress zstd
 - [144] feat(wasm): implement CRC validation plugin in Rust (WASM) — src/wasm/crypto-plugin/ exports verify_crc32()
 - [145] feat(wasm): implement Wasmtime engine singleton — src/wasm/engine.py single Engine, pre-compiled Module cache
 - [146] feat(wasm): implement WASM plugin loader and lifecycle — src/wasm/loader.py per-call Store, fuel limits
 - [147] feat(wasm): add WASI capabilities configuration — src/wasm/wasi_config.py minimal grants: no fs, no net
 - [148] feat(wasm): implement routing plugin host caller — src/wasm/plugins/routing.py marshals Bundle+Neighbor to CBOR
 - [149] feat(wasm): implement compression plugin host caller — src/wasm/plugins/compression.py marshals bytes, handles traps
 - [150] feat(wasm): add plugin signature verification — src/wasm/plugin_verifier.py ed25519 .wasm.sig sidecar check
 - [151] feat(wasm): implement plugin hot-reload watcher — src/wasm/watcher.py watchfiles, re-verify on change
 - [152] feat(wasm): add WASM plugin sandbox escape tests — tests/unit/wasm/test_sandbox.py filesystem/network/CPU limits
 - [153] feat(wasm): add Wasmtime fuel limit and epoch interruption — store.set_fuel(1_000_000), epoch_interruption
 - [154] feat(wasm): compile all WASM modules in Makefile — cargo build --target wasm32-wasip2 --release, sign .wasm
 - [155] feat(wasm): add WASM plugin integration tests — tests/integration/wasm/ load real .wasm, benchmark call overhead

 Phase 9 — AI Agents: Ollama, LangGraph, CrewAI (156–180)

 - [156] feat(ai): implement Ollama client wrapper — src/ai/models/ollama_client.py async generate/chat/embed + streaming
 - [157] feat(ai): add model registry and lifecycle manager — src/ai/models/registry.py pull on startup, LRU eviction
 - [158] feat(ai): implement Modelfile for emergency-tuned model — src/ai/models/Modelfile.emergency FROM llama3.2:3b + SYSTEM
 - [159] feat(ai): define LangGraph mesh coordinator state — src/ai/agents/coordinator_state.py CoordinatorState TypedDict
 - [160] feat(ai): implement LangGraph routing decision node — src/ai/agents/routing_node.py calls Ollama with topology
 - [161] feat(ai): implement LangGraph triage assessment node — src/ai/agents/triage_node.py medical/rescue/supply/comms
 - [162] feat(ai): implement LangGraph resource allocation node — src/ai/agents/resource_node.py bandwidth optimization
 - [163] feat(ai): implement LangGraph anomaly detection node — src/ai/agents/anomaly_node.py partition/malformed/failure detection
 - [164] feat(ai): implement LangGraph human review checkpoint — src/ai/agents/human_review.py interrupt before irreversible actions
 - [165] feat(ai): wire LangGraph coordinator graph — src/ai/agents/coordinator_graph.py StateGraph with conditional edges
 - [166] feat(ai): add LangGraph SQLite checkpointer — SqliteSaver to data/agent_state.db, crash recovery
 - [167] feat(ai): define CrewAI disaster response crew — src/ai/agents/disaster_crew.py TacticalCoordinator + ResourceAnalyst + CommsSpecialist
 - [168] feat(ai): implement CrewAI message prioritization task — src/ai/agents/tasks/prioritize_task.py urgency scores
 - [169] feat(ai): implement CrewAI resource optimization task — src/ai/agents/tasks/resource_task.py bandwidth allocation
 - [170] feat(ai): implement CrewAI situation report task — src/ai/agents/tasks/sitrep_task.py 200-word plain-English SITREP
 - [171] feat(ai): wire CrewAI crew with sequential process — Crew(process=Process.sequential, memory=True)
 - [172] feat(ai): implement CrewAI tool: mesh topology query — src/ai/agents/tools/topology_tool.py calls /api/v1/topology
 - [173] feat(ai): implement CrewAI tool: bundle queue inspect — src/ai/agents/tools/queue_tool.py BundleStore depth + priority
 - [174] feat(ai): implement CrewAI tool: emergency broadcast — src/ai/agents/tools/broadcast_tool.py calls /api/v1/emergency
 - [175] feat(ai): add Arize Phoenix observability integration — src/ai/observability/phoenix.py OTel spans for Ollama calls
 - [176] feat(ai): implement offline AI fallback mode — src/ai/models/fallback.py rule-based trees when Ollama unavailable
 - [177] feat(ai): add AI agent state persistence in DuckDB — src/ai/agents/state_persistence.py CoordinatorState snapshots
 - [178] feat(ai): implement agent performance metrics — src/ai/observability/metrics.py Prometheus ai_decisions_total etc.
 - [179] feat(ai): add AI agent unit tests with mock Ollama — tests/unit/ai/ coordinator_graph, disaster_crew mocked
 - [180] feat(ai): wire AI coordinator into mesh application loop — 30s decision cycle in MeshApplication, MeshEventBus integration

 Phase 10 — MCP Server & Qdrant RAG (181–195)

 - [181] feat(mcp): implement MCP server with FastMCP — src/ai/mcp/server.py FastMCP("EmergencyMeshMCP") on stdio
 - [182] feat(mcp): add MCP tool: send_message — src/ai/mcp/tools/send_message.py wraps bundle submission API
 - [183] feat(mcp): add MCP tool: query_neighbors — src/ai/mcp/tools/neighbors.py structured JSON with LQI
 - [184] feat(mcp): add MCP tool: get_network_status — src/ai/mcp/tools/network_status.py node status + alert level
 - [185] feat(mcp): add MCP resource: mesh_topology — src/ai/mcp/resources/topology.py live topology as Markdown
 - [186] feat(mcp): add MCP resource: knowledge_base — src/ai/mcp/resources/knowledge.py Qdrant RAG fetch
 - [187] feat(mcp): add MCP prompt: emergency_triage — src/ai/mcp/prompts/triage.py system+user prompt with mesh context
 - [188] feat(rag): initialize Qdrant client and collection — src/ai/knowledge/qdrant_client.py emergency_knowledge collection
 - [189] feat(rag): implement document ingestion pipeline — src/ai/knowledge/ingestion.py 512-token chunks, Ollama embed, upsert
 - [190] feat(rag): add emergency knowledge base documents — docs/knowledge/ first_aid, ICS radio, SAR, troubleshooting, supply
 - [191] feat(rag): implement RAG query engine — src/ai/knowledge/rag_engine.py embed+search+format context
 - [192] feat(rag): integrate RAG with CrewAI knowledge tool — src/ai/agents/tools/knowledge_tool.py @tool wrapping RAGEngine
 - [193] feat(rag): add Qdrant collection backup and restore — src/ai/knowledge/backup.py .qdrant.snapshot export/restore
 - [194] feat(mcp): add MCP server integration tests — tests/integration/mcp/ tool and resource call validation
 - [195] feat(rag): add RAG pipeline unit tests — tests/unit/ai/test_rag_engine.py mock Qdrant + Ollama embed

 Phase 11 — Phone PWA (React/TypeScript) (196–220)

 - [196] feat(web): initialize Vite + React + TypeScript project — src/web/ package.json React 18, TS 5, Tailwind, shadcn/ui, Zustand
 - [197] feat(web): configure PWA with service worker — vite-plugin-pwa, manifest.json, standalone display
 - [198] feat(web): implement offline cache strategy — sw.ts Workbox StaleWhileRevalidate + IndexedDB queue
 - [199] feat(web): add IndexedDB offline bundle queue — src/web/services/offlineQueue.ts idb, sync on online event
 - [200] feat(web): implement API client service — src/web/services/api.ts typed wrappers, JWT management, retry
 - [201] feat(web): implement WebSocket client service — src/web/services/websocket.ts reconnect with jitter, heartbeat
 - [202] feat(web): add Zustand store for mesh state — src/web/store/meshStore.ts neighbors, messages, nodeStatus slices
 - [203] feat(web): implement main app layout and navigation — src/web/components/Layout.tsx sidebar + bottom tab bar
 - [204] feat(web): implement message compose component — src/web/components/MessageCompose.tsx EID picker, priority selector
 - [205] feat(web): implement message thread view — src/web/components/MessageThread.tsx delivery status icons, E2E badge
 - [206] feat(web): implement message inbox component — src/web/components/MessageInbox.tsx conversations, unread badges
 - [207] feat(web): implement network topology map — src/web/components/TopologyMap.tsx react-force-graph-2d
 - [208] feat(web): implement geospatial node map — src/web/components/GeoMap.tsx react-leaflet, offline tiles
 - [209] feat(web): implement node status dashboard — src/web/components/StatusDashboard.tsx transports, store depth, AI state
 - [210] feat(web): implement emergency alert panel — src/web/components/EmergencyPanel.tsx SOS button, vibration API
 - [211] feat(web): implement settings page — src/web/components/Settings.tsx LoRa config, AI model, routing strategy
 - [212] feat(web): add push notification support — src/web/services/notifications.ts Notification API, deep-link actions
 - [213] feat(web): implement dark mode and theme system — src/web/hooks/useTheme.ts CSS variables, prefers-color-scheme
 - [214] feat(web): add accessibility (a11y) improvements — aria-label, role, tabIndex, focus trap, react-aria
 - [215] feat(web): implement E2E encryption UI indicators — src/web/components/EncryptionBadge.tsx verified/warning/fingerprint
 - [216] feat(web): add web unit tests with Vitest and Testing Library — src/web/tests/ MessageCompose, StatusDashboard, api.test
 - [217] feat(web): add Storybook for component development — .storybook/ config + stories for 4 key components
 - [218] feat(web): implement localization (i18n) framework — react-i18next, en/es/zh-TW translations
 - [219] feat(web): add PWA install prompt component — src/web/components/InstallPrompt.tsx beforeinstallprompt handler
 - [220] feat(web): configure production build optimization — Rollup code splitting, terser, gzip/brotli compression

 Phase 12 — Cilium Tetragon & Audit Layer (221–230)

 - [221] feat(security): implement Tetragon event stream reader — src/security/audit/tetragon.py gRPC ProcessEvent/NetworkEvent
 - [222] feat(security): define mesh-specific Tetragon TracingPolicies — deploy/tetragon/policies/mesh-network-policy.yaml
 - [223] feat(security): implement audit log writer — src/security/audit/writer.py enriches events, writes Redis + DuckDB
 - [224] feat(security): add security event classifier — src/security/audit/classifier.py port scan, retry flood, unknown EID
 - [225] feat(security): implement anomaly alerting pipeline — src/security/audit/alerter.py high-severity → MeshEventBus
 - [226] feat(security): add intrusion detection rules — src/security/audit/ids_rules.py replay, signature flood, routing loop
 - [227] feat(security): implement audit dashboard endpoint — GET /api/v1/audit/events admin-only, DuckDB date range
 - [228] feat(security): add Tetragon integration tests — tests/integration/security/test_tetragon.py mock gRPC stream
 - [229] feat(security): implement process allowlist enforcement — src/security/audit/allowlist.py binary hash validation
 - [230] feat(security): add audit log tamper detection — src/security/audit/integrity.py SHA-256 chained hashes

 Phase 13 — Federated Learning with Flower (231–240)

 - [231] feat(fl): define federated learning task for routing models — src/ai/federated/task.py PyTorch delivery probability model
 - [232] feat(fl): implement Flower client for mesh nodes — src/ai/federated/flower_client.py NumPyClient on DuckDB telemetry
 - [233] feat(fl): implement Flower server for base station nodes — src/ai/federated/flower_server.py FedAvg, 3 rounds, min 2 clients
 - [234] feat(fl): add differential privacy to federated training — opacus DP-SGD epsilon=1.0, delta=1e-5
 - [235] feat(fl): implement model aggregation and distribution — src/ai/federated/aggregator.py Redis pub/sub notify
 - [236] feat(fl): add federated model loading in routing decisions — routing_node.py loads routing_model.pth if available
 - [237] feat(fl): implement model versioning and rollback — src/ai/federated/versioning.py DuckDB registry + rollback()
 - [238] feat(fl): add federated learning integration tests — tests/integration/ai/test_flower_federation.py in-process 2 clients
 - [239] feat(fl): implement secure aggregation stub — src/ai/federated/secure_aggregation.py Shamir secret sharing
 - [240] feat(fl): add Flower training metrics to Arize Phoenix — OTel spans for loss, accuracy, round number

 Phase 14 — Unit Tests (pytest) (241–255)

 - [241] test(unit): add mesh protocol bundle serialization tests — CBOR round-trip, malformed rejection, fragment reassembly
 - [242] test(unit): add routing algorithm unit tests — Epidemic/PRoPHET/SprayWait with mock neighbor tables
 - [243] test(unit): add bundle store unit tests — enqueue/dequeue, TTL expiry, capacity limit, concurrent access
 - [244] test(unit): add contact graph unit tests — add/remove edges, Dijkstra, partition detection
 - [245] test(unit): add transport adapter unit tests — UDP/TCP with SimulatedTransport, fragmentation, priority queue
 - [246] test(unit): add LoRa packet codec unit tests — all PacketType values, CRC corruption, boundary values
 - [247] test(unit): add ARQ session unit tests — happy path, timeout/retry, sequence rollover, duplicate suppression
 - [248] test(unit): add crypto unit tests — signing and verification — sign/verify, tampered rejection, timing-safe comparison
 - [249] test(unit): add crypto unit tests — X3DH and Double Ratchet — full handshake, message key derivation, out-of-order
 - [250] test(unit): add data layer unit tests — Redis client — mock redis.asyncio, pubsub, geo index, rate limiter
 - [251] test(unit): add data layer unit tests — DuckDB analytics — in-memory DuckDB, delivery ratio, latency histogram
 - [252] test(unit): add AI agent unit tests — LangGraph graph — mock all nodes, edge routing, state persistence
 - [253] test(unit): add Ollama client unit tests — mock httpx.AsyncClient, streaming parsing, error handling
 - [254] test(unit): add API endpoint unit tests — TestClient, JWT validation, rate limits, security headers
 - [255] test(unit): add property-based tests with Hypothesis — Bundle, LoRaPacket, RoutingEntry strategies + invariants

 Phase 15 — Robot Framework: Functional & E2E (256–270)

 - [256] test(robot): initialize Robot Framework test infrastructure — tests/robot/robot.yaml, common.resource with auth/setup keywords
 - [257] test(robot): add custom Robot Framework library for mesh — tests/robot/libraries/MeshLibrary.py Send Bundle, Wait For Delivery etc.
 - [258] test(robot): add custom library for LoRa simulation — tests/robot/libraries/LoRaLibrary.py Set Packet Loss Rate etc.
 - [259] test(robot): implement node startup functional test suite — functional/node_startup.robot EID gen, transport, API ready
 - [260] test(robot): implement message delivery functional tests — functional/message_delivery.robot single/multi-hop, priority
 - [261] test(robot): implement emergency alert functional tests — functional/emergency_alerts.robot broadcast, dedup, queue jump
 - [262] test(robot): implement neighbor discovery functional tests — functional/neighbor_discovery.robot join, departure, LQI update
 - [263] test(robot): implement LoRa transport functional tests — functional/lora_transport.robot ARQ, duty cycle, ADR, FHSS
 - [264] test(robot): implement DTN store-and-forward tests — functional/store_and_forward.robot outage queue, reconnect deliver, expiry
 - [265] test(robot): implement encryption functional tests — functional/encryption.robot encrypted exchange, tamper reject, rotation
 - [266] test(robot): implement AI coordinator functional tests — functional/ai_coordinator.robot strategy selection, SITREP, triage
 - [267] test(robot): implement full E2E disaster scenario test — e2e/disaster_scenario.robot 5-node mesh, outage, 3-hop, AI triage
 - [268] test(robot): implement web PWA E2E tests with Browser library — e2e/pwa_e2e.robot Playwright, send+verify+offline sync
 - [269] test(robot): implement API contract tests — functional/api_contracts.robot schemathesis against openapi.yaml
 - [270] test(robot): add performance threshold acceptance tests — functional/performance_thresholds.robot <5s delivery, <200ms API

 Phase 16 — Robot Framework: OWASP Top 10 (271–285)

 - [271] test(security): add OWASP test infrastructure and base keywords — tests/robot/security/owasp_base.resource + ZAP setup
 - [272] test(security): OWASP A01 — Broken Access Control tests — A01_broken_access_control.robot unauth access, IDOR, BOLA
 - [273] test(security): OWASP A01 — force-browsing and privilege escalation — horizontal escalation, admin endpoint without admin JWT
 - [274] test(security): OWASP A02 — Cryptographic Failures tests — A02_cryptographic_failures.robot plaintext, weak cipher, key in response
 - [275] test(security): OWASP A02 — TLS and key management tests — TLS 1.0/1.1 rejection, predictable nonce detection
 - [276] test(security): OWASP A03 — Injection tests — A03_injection.robot SQL/NoSQL injection, command injection, CBOR bomb
 - [277] test(security): OWASP A03 — XSS and template injection tests — stored XSS via message, SSTI in SITREP, header injection
 - [278] test(security): OWASP A04 — Insecure Design tests — A04_insecure_design.robot rate-limit bypass, store exhaustion, replay
 - [279] test(security): OWASP A05 — Security Misconfiguration tests — A05_security_misconfiguration.robot debug endpoints, stack trace, CORS wildcard
 - [280] test(security): OWASP A06 — Vulnerable Components scan — A06_vulnerable_components.robot pip-audit + npm audit, SBOM check
 - [281] test(security): OWASP A07 — Authentication Failures tests — A07_auth_failures.robot brute force, JWT alg confusion, null JWT
 - [282] test(security): OWASP A08 — Software Integrity tests — A08_software_integrity.robot unsigned WASM load, tampered plugin
 - [283] test(security): OWASP A09 — Security Logging Failures tests — A09_logging_failures.robot failed auth logged, key material absent from logs
 - [284] test(security): OWASP A10 — SSRF tests — A10_ssrf.robot Ollama URL override, Qdrant injection, 169.254.169.254
 - [285] test(security): add OWASP ZAP active scan integration — zap_active_scan.robot Docker ZAP, spider, active scan, CRITICAL block

 Phase 17 — CI/CD Pipelines (GitHub Actions) (286–295)

 - [286] ci: implement main CI workflow (lint, type, unit tests) — replaces ci.yml; jobs: lint, unit-tests, web-tests; Python 3.12/Node 20 matrix
 - [287] ci: add integration test job to CI workflow — integration-tests job; services: redis:7, qdrant:latest; 20min timeout
 - [288] ci: implement security scan workflow — security.yml: pip-audit, npm-audit, gitleaks, trivy, bandit, semgrep
 - [289] ci: add OWASP ZAP scan workflow — security.yml ZAP job; ephemeral Docker Compose; baseline + full scan artifact
 - [290] ci: implement Robot Framework test workflow — robot-tests.yml; RF + Browser library; full docker-compose; functional + E2E
 - [291] ci: add OWASP Robot security tests to CI — robot-tests.yml security-tests job; blocks merge on A01–A10 failures
 - [292] ci: implement performance test workflow — performance.yml; Locust 50 users, 5min; p95 < 500ms assertion + baseline compare
 - [293] ci: add WASM build and verification workflow — wasm-build.yml; Rust compile, ed25519 sign from secret, upload to release
 - [294] ci: implement Docker build and push workflow — docker.yml; build 3 Dockerfiles; push GHCR on main; SHA + latest tags
 - [295] ci: add deployment workflow with health gate — deploy.yml; SSH + docker compose up; /healthz + /readyz check; rollback on failure

 Phase 18 — Docker, Observability & Docs (296–300)

 - [296] feat(docker): add production Dockerfiles for all services — docker/Dockerfile.api (python:3.12-slim), Dockerfile.mesh (Go+Python multistage), Dockerfile.web (nginx)
     Phase 18 — Docker, Observability & Docs (296–300)

     - [296] feat(docker): add production Dockerfiles for all services — docker/Dockerfile.api (python:3.12-slim), Dockerfile.mesh (Go+Python multistage), Dockerfile.web (nginx)
     - [297] feat(docker): add comprehensive docker-compose for full stack — docker/docker-compose.yml: api, mesh, web, redis, qdrant, ollama, phoenix, prometheus, grafana
     - [298] feat(observability): add Prometheus and Grafana configuration — deploy/prometheus/prometheus.yml; grafana/dashboards/mesh-overview.json LQI heatmap, delivery ratio
     - [299] feat(observability): integrate Arize Phoenix for LLM tracing — deploy/phoenix/config.yaml; OTLP export; grafana/dashboards/ai-agents.json
     - [300] docs: finalize README with full getting-started guide — rewrite README.md: architecture diagram, quickstart, hardware wiring, Pi setup, contributing, license

     ---
     Critical Files (implementation starting points)

     ┌──────────────────────────────────────────┬───────┬───────────────────────────────────────────────┐
     │                   File                   │ Phase │                 Why Critical                  │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/config.py                            │ 1     │ Shared settings used everywhere               │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/mesh/protocol/bundle.py              │ 2     │ Core data structure for all routing           │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/mesh/router/forwarder.go             │ 2     │ Go hot path for all bundle forwarding         │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/mesh/transport/base.py               │ 3     │ Contract every transport adapter must fulfill │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/lora/lora_transport.py               │ 4     │ Primary hardware integration point            │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/data/redis/client.py                 │ 5     │ Shared by 15+ modules                         │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/security/crypto/x3dh.py              │ 6     │ Establishes E2E sessions before API goes live │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/api/main.py                          │ 7     │ FastAPI app wiring all routes                 │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/ai/agents/coordinator_graph.py       │ 9     │ LangGraph StateGraph — AI nervous system      │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ src/ai/mcp/server.py                     │ 10    │ MCP interface for agent tool ecosystem        │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ tests/robot/security/owasp_base.resource │ 16    │ Pattern for all 10 OWASP test files           │
     ├──────────────────────────────────────────┼───────┼───────────────────────────────────────────────┤
     │ .github/workflows/ci.yml                 │ 17    │ Gate for all merges                           │
     └──────────────────────────────────────────┴───────┴───────────────────────────────────────────────┘

     ---
     Verification Plan

     1. Unit tests: make test → pytest tests/unit/ --cov=src --cov-fail-under=80
     2. Integration tests: make test-integration → docker compose -f docker/docker-compose.yml up -d && pytest tests/integration/
     3. Robot Framework functional: make robot → robot tests/robot/functional/
     4. Robot Framework E2E: robot tests/robot/e2e/ (requires full stack running)
     5. OWASP security: robot tests/robot/security/ (requires ZAP running)
     6. CI gate: All GitHub Actions workflows green on PR to main
     7. Smoke test: make docker-up → send message via PWA → verify delivery in thread view → check /api/v1/analytics shows delivery