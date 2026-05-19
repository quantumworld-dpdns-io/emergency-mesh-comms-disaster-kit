import { useTheme } from "../hooks/useTheme";

export default function Settings() {
  const { theme, setTheme } = useTheme();
  return <div className="card"><h3>Settings</h3><label>Theme<select value={theme} onChange={(e) => setTheme(e.target.value)}><option value="dark">dark</option><option value="light">light</option></select></label></div>;
}
