# Disaster Deployment Runbook

1. Bring up core services: Redis, Qdrant, API, Mesh, Web.
2. Validate `/healthz` and `/readyz`.
3. Verify neighbor discovery and bundle forwarding.
4. Enable emergency broadcast controls.
5. Monitor telemetry and security alerts.
