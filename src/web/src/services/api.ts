import { enqueue } from "./offlineQueue";

const API = "/api/v1";

let jwtToken = "";
export function setToken(token: string) { jwtToken = token; }

function headers() {
  return {
    "Content-Type": "application/json",
    ...(jwtToken ? { Authorization: `Bearer ${jwtToken}` } : {}),
    "X-API-Key": "dev-api-key"
  };
}

export async function fetchStatus() {
  const r = await fetch(`${API}/status`, { headers: headers() });
  return r.json();
}

export async function fetchNeighbors() {
  const r = await fetch(`${API}/neighbors`, { headers: headers() });
  return r.json();
}

export async function sendMessage(to_eid: string, text: string, priority = "general") {
  const body = { to_eid, text, priority };
  try {
    const r = await fetch(`${API}/messages`, { method: "POST", headers: headers(), body: JSON.stringify(body) });
    if (!r.ok) throw new Error("send failed");
    return r.json();
  } catch {
    await enqueue({ id: crypto.randomUUID(), path: "/messages", body });
    return { queued_offline: true };
  }
}
