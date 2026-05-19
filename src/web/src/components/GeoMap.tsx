import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useMemo } from "react";
import { useMeshStore } from "../store/meshStore";

type GeoPoint = { id: string; lat: number; lng: number; eid: string; lqi: number };

// Deterministic pseudo-geo placement around a center for offline visualization.
function pseudoCoords(nodeId: string): { lat: number; lng: number } {
  const seed = Array.from(nodeId).reduce((a, c) => a + c.charCodeAt(0), 0);
  const lat = 25.033 + ((seed % 17) - 8) * 0.0025;
  const lng = 121.5654 + ((seed % 19) - 9) * 0.0025;
  return { lat, lng };
}

export default function GeoMap() {
  const neighbors = useMeshStore((s) => s.neighbors);

  const points = useMemo<GeoPoint[]>(() => {
    return neighbors.map((n) => {
      const c = pseudoCoords(n.node_id);
      return { id: n.node_id, eid: n.eid, lqi: n.lqi, lat: c.lat, lng: c.lng };
    });
  }, [neighbors]);

  return (
    <div className="card" role="region" aria-label="geo map">
      <h3>Geo Map</h3>
      <p style={{ color: "var(--muted)" }}>Offline-capable node map with deterministic local placement.</p>
      <div style={{ height: 320, borderRadius: 10, overflow: "hidden" }}>
        <MapContainer center={[25.033, 121.5654]} zoom={13} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {points.map((p) => (
            <Marker key={p.id} position={[p.lat, p.lng]}>
              <Popup>
                <strong>{p.id}</strong>
                <br />
                {p.eid}
                <br />
                LQI: {p.lqi}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
      <small style={{ color: "var(--muted)" }}>Displayed nodes: {points.length}</small>
    </div>
  );
}
