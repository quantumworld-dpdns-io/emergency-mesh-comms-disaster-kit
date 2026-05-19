import { useEffect, useState } from "react";

export function useTheme() {
  const [theme, setTheme] = useState<string>(localStorage.getItem("theme") || "dark");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  return { theme, setTheme };
}
