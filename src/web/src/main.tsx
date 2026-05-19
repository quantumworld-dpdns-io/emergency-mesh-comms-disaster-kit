import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { useTranslation } from "react-i18next";
import "./styles/app.css";
import "./i18n";

import Layout from "./components/Layout";
import MessageCompose from "./components/MessageCompose";
import MessageThread from "./components/MessageThread";
import MessageInbox from "./components/MessageInbox";
import TopologyMap from "./components/TopologyMap";
import GeoMap from "./components/GeoMap";
import StatusDashboard from "./components/StatusDashboard";
import EmergencyPanel from "./components/EmergencyPanel";
import Settings from "./components/Settings";
import InstallPrompt from "./components/InstallPrompt";
import { connectWS } from "./services/websocket";
import { drain } from "./services/offlineQueue";
import { fetchNeighbors, fetchStatus, sendMessage, setToken } from "./services/api";
import { useMeshStore } from "./store/meshStore";

function App() {
  const { t, i18n } = useTranslation();
  const setNeighbors = useMeshStore((s) => s.setNeighbors);
  const setStatus = useMeshStore((s) => s.setNodeStatus);
  const [tab, setTab] = useState("compose");

  useEffect(() => {
    (async () => {
      const tokenResp = await fetch("/api/v1/auth/token?node_id=web-client&admin=true", { method: "POST" });
      const tok = await tokenResp.json();
      setToken(tok.token);
      setNeighbors(await fetchNeighbors());
      setStatus(await fetchStatus());
    })();

    const stop = connectWS(() => {
      fetchStatus().then(setStatus).catch(() => undefined);
    });

    const onOnline = async () => {
      const items = await drain();
      for (const it of items) {
        await sendMessage(String(it.body.to_eid), String(it.body.text), String(it.body.priority || "general"));
      }
    };
    window.addEventListener("online", onOnline);
    return () => { stop(); window.removeEventListener("online", onOnline); };
  }, [setNeighbors, setStatus]);

  return (
    <Layout>
      <div className="tabs">
        <button onClick={() => setTab("compose")}>{t("compose")}</button>
        <button onClick={() => setTab("inbox")}>{t("inbox")}</button>
        <button onClick={() => setTab("network")}>Network</button>
        <button onClick={() => setTab("settings")}>{t("settings")}</button>
        <select aria-label="language" onChange={(e) => i18n.changeLanguage(e.target.value)} defaultValue="en">
          <option value="en">en</option><option value="es">es</option><option value="zh-TW">zh-TW</option>
        </select>
      </div>

      <InstallPrompt />
      <StatusDashboard />
      <EmergencyPanel />

      {tab === "compose" && <MessageCompose />}
      {tab === "inbox" && <><MessageInbox /><MessageThread /></>}
      {tab === "network" && <><TopologyMap /><GeoMap /></>}
      {tab === "settings" && <Settings />}
    </Layout>
  );
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
