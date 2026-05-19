import { useMeshStore } from "../store/meshStore";

export default function MessageInbox() {
  const messages = useMeshStore((s) => s.messages);
  return <div className="card"><h3>Inbox</h3><p>Unread: {messages.length}</p></div>;
}
