from __future__ import annotations

import pytest

from src.ai.mcp.prompts.triage import emergency_triage_prompt
from src.ai.mcp.resources.topology import topology_markdown
from src.ai.mcp.server import EmergencyMeshMCPServer


@pytest.mark.integration
def test_topology_resource_renders_markdown() -> None:
    md = topology_markdown(
        {"nodes": [{"id": "node-1"}, {"id": "node-2"}], "edges": [{"from": "node-1", "to": "node-2", "lqi": 70}]}
    )
    assert "Mesh Topology" in md
    assert "node-1 -> node-2" in md


@pytest.mark.integration
def test_triage_prompt_contains_context() -> None:
    prompt = emergency_triage_prompt("topology:2 nodes", "severe bleeding")
    assert "topology:2 nodes" in prompt
    assert "severe bleeding" in prompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_server_name() -> None:
    server = EmergencyMeshMCPServer()
    assert server.name == "EmergencyMeshMCP"
