import { useMeshStore } from "../store/meshStore";

export default function StatusDashboard() {
  const status = useMeshStore((s) => s.nodeStatus);
  return <div className="card"><h3>Status</h3><p>Routing: {status.routing_strategy}</p><p>Store Depth: {status.store_depth}</p><p>Battery: {status.battery}</p></div>;
}
