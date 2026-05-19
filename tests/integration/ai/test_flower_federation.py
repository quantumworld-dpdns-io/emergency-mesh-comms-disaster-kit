from __future__ import annotations

import duckdb
import pytest

from src.ai.federated.aggregator import ModelAggregator
from src.ai.federated.flower_client import MeshFlowerClient
from src.ai.federated.flower_server import MeshFlowerServer
from src.ai.federated.secure_aggregation import ShamirSecureAggregationStub
from src.ai.federated.task import RoutingModelTask, RoutingSample
from src.ai.federated.versioning import FederatedModelVersioning
from src.ai.observability.phoenix import PhoenixTracer


@pytest.mark.integration
def test_flower_training_two_clients_and_versioning() -> None:
    samples_a = [
        RoutingSample(lqi=70, queue_depth=20, topology_size=6, delivered=1),
        RoutingSample(lqi=40, queue_depth=200, topology_size=2, delivered=0),
    ]
    samples_b = [
        RoutingSample(lqi=80, queue_depth=10, topology_size=8, delivered=1),
        RoutingSample(lqi=35, queue_depth=260, topology_size=3, delivered=0),
    ]

    c1 = MeshFlowerClient("node-a", RoutingModelTask(), samples_a)
    c2 = MeshFlowerClient("node-b", RoutingModelTask(), samples_b)

    tracer = PhoenixTracer()
    server = MeshFlowerServer(min_clients=2, rounds=3, tracer=tracer)
    final_weights = server.train([c1, c2], initial_weights=[0.1, -0.1, 0.1, 0.0])

    assert len(final_weights) == 4
    assert len(server.metrics) == 3
    assert any(e.name == "fl_round_metrics" for e in tracer.events)

    conn = duckdb.connect(":memory:")
    versioning = FederatedModelVersioning(conn, model_dir="/tmp/mesh-fl-models")
    path = versioning.save_version("v1", final_weights, active=True)
    assert path.exists()
    assert versioning.active_model_path() is not None


@pytest.mark.integration
def test_secure_aggregation_stub_round_trip() -> None:
    secret = 0.742
    shares = ShamirSecureAggregationStub.split(secret, n_shares=4)
    restored = ShamirSecureAggregationStub.combine(shares)
    assert abs(restored - secret) < 1e-9


@pytest.mark.integration
def test_aggregator_publish_notification() -> None:
    agg = ModelAggregator()
    agg.publish([0.1, 0.2, 0.3, 0.0], version="v2")
    assert agg.latest_weights is not None
    assert agg.notifications[-1]["version"] == "v2"
