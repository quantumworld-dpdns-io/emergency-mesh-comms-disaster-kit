import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

vi.mock("react-leaflet", () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => <div data-testid="map-container">{children}</div>,
  TileLayer: () => <div data-testid="tile-layer" />, 
  Marker: ({ children }: { children: React.ReactNode }) => <div data-testid="marker">{children}</div>,
  Popup: ({ children }: { children: React.ReactNode }) => <div>{children}</div>
}));

import GeoMap from "../components/GeoMap";
import { useMeshStore } from "../store/meshStore";

test("renders geo map markers from neighbors", () => {
  useMeshStore.setState({
    neighbors: [
      { node_id: "node-2", eid: "dtn://node-2", lqi: 70 },
      { node_id: "node-3", eid: "dtn://node-3", lqi: 60 }
    ]
  });

  render(<GeoMap />);
  expect(screen.getByText("Geo Map")).toBeInTheDocument();
  expect(screen.getByTestId("map-container")).toBeInTheDocument();
  expect(screen.getAllByTestId("marker")).toHaveLength(2);
});
