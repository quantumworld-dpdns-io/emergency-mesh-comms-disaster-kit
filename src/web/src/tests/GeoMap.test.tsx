import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

vi.mock("react-leaflet", () => ({
  MapContainer: ({ children }: { children: unknown }) => <div data-testid="map-container">{children as any}</div>,
  TileLayer: () => <div data-testid="tile-layer" />, 
  Marker: ({ children }: { children: unknown }) => <div data-testid="marker">{children as any}</div>,
  Popup: ({ children }: { children: unknown }) => <div>{children as any}</div>
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
