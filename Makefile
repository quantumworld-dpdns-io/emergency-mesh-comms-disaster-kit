.PHONY: dev test lint build-wasm robot security-scan docker-up test-integration

dev:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8080

test:
	pytest tests/unit -q

test-integration:
	pytest tests/integration -q

lint:
	ruff check src tests
	mypy src

build-wasm:
	cargo build --manifest-path src/wasm/Cargo.toml --target wasm32-wasip2 --release
	for f in src/wasm/target/wasm32-wasip2/release/*.wasm; do \
		[ -f "$$f" ] || continue; \
		openssl dgst -sha256 -binary "$$f" > "$$f.sig"; \
	done

robot:
	robot tests/robot/functional

security-scan:
	pip-audit
	bandit -r src

docker-up:
	docker compose -f docker/docker-compose.yml up -d
