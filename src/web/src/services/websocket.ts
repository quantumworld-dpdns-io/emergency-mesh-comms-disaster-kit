export function connectWS(onEvent: (ev: unknown) => void) {
  let ws: WebSocket | null = null;
  let tries = 0;

  const open = () => {
    ws = new WebSocket(`${location.origin.replace("http", "ws")}/api/v1/ws`);
    ws.onmessage = (m) => {
      try { onEvent(JSON.parse(m.data)); } catch { onEvent(m.data); }
    };
    ws.onclose = () => {
      tries += 1;
      const wait = Math.min(10000, 300 + tries * 400 + Math.random() * 200);
      setTimeout(open, wait);
    };
  };

  open();
  return () => ws?.close();
}
