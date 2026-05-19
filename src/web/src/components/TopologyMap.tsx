import ForceGraph2D from "react-force-graph-2d";
import { useMemo } from "react";
import { useMeshStore } from "../store/meshStore";

type TopologyNode = { id: string; group: number };
type TopologyLink = { source: string; target: string; value: number };

export default function TopologyMap() {
  const neighbors = useMeshStore((s) => s.neighbors);

  const graph = useMemo(() => {
    const nodes: TopologyNode[] = [{ id: "node-1", group: 1 }];
    const links: TopologyLink[] = [];
    for (const n of neighbors) {
      nodes.push({ id: n.node_id, group: 2 });
      links.push({ source: "node-1", target: n.node_id, value: Math.max(1, Math.round(n.lqi / 10)) });
    }
    return { nodes, links };
  }, [neighbors]);

  return (
    <div className="card" role="region" aria-label="topology map">
      <h3>Topology Map</h3>
      <p style={{ color: "var(--muted)" }}>
        Live neighbor graph with link weight derived from LQI.
      </p>
      <div style={{ height: 320, borderRadius: 10, overflow: "hidden", background: "#102735" }}>
        <ForceGraph2D
          graphData={graph}
          nodeLabel={(node) => String((node as TopologyNode).id)}
          linkWidth={(link) => Number((link as TopologyLink).value)}
          nodeAutoColorBy="group"
          cooldownTicks={80}
          width={700}
          height={320}
        />
      </div>
      <small style={{ color: "var(--muted)" }}>Nodes: {graph.nodes.length} | Links: {graph.links.length}</small>
    </div>
  );
}
