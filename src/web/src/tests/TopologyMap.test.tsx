import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

vi.mock("react-force-graph-2d", () => ({
  default: ({ graphData }: { graphData: { nodes: unknown[]; links: unknown[] } }) => (
    <div data-testid="force-graph">nodes:{graphData.nodes.length};links:{graphData.links.length}</div>
  )
}));

import TopologyMap from "../components/TopologyMap";
import { useMeshStore } from "../store/meshStore";

test("renders topology graph with nodes", () => {
  useMeshStore.setState({
    neighbors: [
      { node_id: "node-2", eid: "dtn://node-2", lqi: 70 },
      { node_id: "node-3", eid: "dtn://node-3", lqi: 60 }
    ]
  });

  render(<TopologyMap />);
  expect(screen.getByText("Topology Map")).toBeInTheDocument();
  expect(screen.getByTestId("force-graph")).toHaveTextContent("nodes:3;links:2");
});
