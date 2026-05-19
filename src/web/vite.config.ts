import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Emergency Mesh Comms",
        short_name: "MeshComms",
        display: "standalone",
        start_url: "/",
        background_color: "#10222d",
        theme_color: "#ed6a5a",
        icons: []
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,png,svg}"],
        runtimeCaching: [{ urlPattern: /\/api\//, handler: "StaleWhileRevalidate" }]
      }
    })
  ],
  build: {
    target: "es2022",
    minify: "terser",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "zustand"]
        }
      }
    }
  }
});
