import { useState } from "react";
import { sendMessage } from "../services/api";
import { useMeshStore } from "../store/meshStore";

export default function MessageCompose() {
  const [to, setTo] = useState("dtn://node-2");
  const [text, setText] = useState("");
  const [priority, setPriority] = useState("general");
  const addMessage = useMeshStore((s) => s.addMessage);

  return (
    <div className="card" role="region" aria-label="message compose">
      <h3>Compose</h3>
      <label>Destination EID<input aria-label="Destination EID" value={to} onChange={(e) => setTo(e.target.value)} /></label>
      <label>Priority<select aria-label="Priority" value={priority} onChange={(e) => setPriority(e.target.value)}><option>general</option><option>medical</option><option>emergency</option></select></label>
      <label>Message<textarea aria-label="Message" value={text} onChange={(e) => setText(e.target.value)} /></label>
      <button onClick={async () => {
        const res = await sendMessage(to, text, priority);
        addMessage({ id: res.message_id || crypto.randomUUID(), to, text, status: res.queued_offline ? "offline-queued" : "queued", encrypted: true });
        setText("");
      }}>Send</button>
    </div>
  );
}
