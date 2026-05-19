import EncryptionBadge from "./EncryptionBadge";
import { useMeshStore } from "../store/meshStore";

export default function MessageThread() {
  const messages = useMeshStore((s) => s.messages);
  return <div className="card"><h3>Thread</h3>{messages.map((m) => <div key={m.id}><strong>{m.to}</strong> - {m.text} <span className="badge">{m.status}</span> <EncryptionBadge verified={!!m.encrypted} /></div>)}</div>;
}
