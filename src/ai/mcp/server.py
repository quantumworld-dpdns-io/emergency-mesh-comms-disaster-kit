from __future__ import annotations

from dataclasses import dataclass

from src.ai.agents.tools.knowledge_tool import query_knowledge
from src.ai.knowledge.rag_engine import RAGEngine
from src.ai.mcp.prompts.triage import emergency_triage_prompt
from src.ai.mcp.resources.knowledge import knowledge_markdown
from src.ai.mcp.resources.topology import topology_markdown
from src.ai.mcp.tools.neighbors import query_neighbors
from src.ai.mcp.tools.network_status import get_network_status
from src.ai.mcp.tools.send_message import send_message


@dataclass(slots=True)
class EmergencyMeshMCPServer:
    name: str = "EmergencyMeshMCP"

    async def tool_send_message(
        self, api_base_url: str, bearer_token: str, to_eid: str, text: str
    ) -> dict[str, object]:
        return await send_message(api_base_url, bearer_token, to_eid, text)

    async def tool_query_neighbors(self, api_base_url: str, bearer_token: str) -> list[dict[str, object]]:
        return await query_neighbors(api_base_url, bearer_token)

    async def tool_get_network_status(self, api_base_url: str, bearer_token: str) -> dict[str, object]:
        return await get_network_status(api_base_url, bearer_token)

    def resource_mesh_topology(self, topology_json: dict[str, object]) -> str:
        return topology_markdown(topology_json)

    async def resource_knowledge_base(self, rag: RAGEngine, question: str) -> str:
        result = await query_knowledge(rag, question)
        return knowledge_markdown(str(result["answer"]), list(result["context_docs"]))

    def prompt_emergency_triage(self, mesh_context: str, incident_text: str) -> str:
        return emergency_triage_prompt(mesh_context, incident_text)
