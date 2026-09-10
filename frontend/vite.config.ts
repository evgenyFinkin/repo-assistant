import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Frontend runs in its own container (compose.yml); "localhost" here
      // would mean the frontend container itself, not the backend. Use the
      // compose service name so container-to-container requests resolve.
      "/api": process.env.VITE_API_PROXY_TARGET ?? "http://backend:8000",
    },
  },
});
