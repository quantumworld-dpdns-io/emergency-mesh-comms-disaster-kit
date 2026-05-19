from locust import HttpUser, between, task


class MeshApiUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        resp = self.client.post("/api/v1/auth/token?node_id=locust&admin=false")
        token = resp.json()["token"]
        self.headers = {"Authorization": f"Bearer {token}", "X-API-Key": "dev-api-key"}

    @task(3)
    def read_status(self):
        self.client.get("/api/v1/status", headers=self.headers)

    @task(2)
    def read_neighbors(self):
        self.client.get("/api/v1/neighbors", headers=self.headers)

    @task(1)
    def send_message(self):
        self.client.post(
            "/api/v1/messages",
            headers=self.headers,
            json={"to_eid": "dtn://node-2", "text": "locust", "priority": "general"},
        )
