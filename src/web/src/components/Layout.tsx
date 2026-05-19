import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="app">
      <aside className="sidebar">
        <h2>MeshComms</h2>
        <p style={{ color: "var(--muted)" }}>Offline-first emergency communications.</p>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
