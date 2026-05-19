from __future__ import annotations


def topology_markdown(topology: dict[str, object]) -> str:
    nodes = topology.get("nodes", [])
    edges = topology.get("edges", [])
    lines = ["# Mesh Topology", "", f"Nodes: {len(nodes)}", f"Edges: {len(edges)}", "", "## Edges"]
    for e in edges:
        lines.append(f"- {e.get('from')} -> {e.get('to')} (lqi={e.get('lqi')})")
    return "\n".join(lines)
