import { useEffect, useState } from "react";

export default function InstallPrompt() {
  const [evt, setEvt] = useState<any>(null);
  useEffect(() => {
    const handler = (e: Event) => { e.preventDefault(); setEvt(e); };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);
  if (!evt) return null;
  return <button onClick={() => evt.prompt()}>Install App</button>;
}
