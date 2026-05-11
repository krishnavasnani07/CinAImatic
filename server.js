import express from 'express';
import { createServer } from 'http';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createProxyMiddleware } from 'http-proxy-middleware';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const API_PORT = process.env.API_PORT || 8001;

// ── Proxy /api/* → FastAPI Python backend ────────────────────────────────────
app.use('/api', createProxyMiddleware({
  target: `http://localhost:${API_PORT}`,
  changeOrigin: true,
  // Ensure the /api prefix is added back when forwarding to Python
  pathRewrite: { '^/': '/api/' }, 
  on: {
    proxyReq: (proxyReq, req, res) => {
      console.log(`[proxy] Forwarding ${req.method} /api${req.url} -> http://localhost:${API_PORT}/api${req.url}`);
    },
    error: (err, req, res) => {
      console.error('[proxy] ERROR:', err.message);
      if (!res.headersSent) {
        res.status(503).json({ error: 'AI engine unreachable', details: err.message });
      }
    }
  }
}));

// ── Proxy /ws/* → FastAPI WebSocket backend ──────────────────────────────────
app.use('/ws', createProxyMiddleware({
  target: `http://localhost:${API_PORT}`,
  changeOrigin: true,
  ws: true,
}));

// Serve static files from the Vite build directory
app.use(express.static(join(__dirname, 'dist')));

// Fallback: serve index.html for all other routes (for SPA routing)
app.use((req, res) => {
  res.sendFile(join(__dirname, 'dist', 'index.html'));
});

const server = createServer(app);
server.listen(PORT, () => {
  console.log(`\x1b[32m✅  CINECAST frontend running at  http://localhost:${PORT}\x1b[0m`);
  console.log(`\x1b[35m🐍  FastAPI bridge running at      http://localhost:${API_PORT}\x1b[0m`);
  console.log(`\x1b[36m🔌  WebSocket terminal at         ws://localhost:${PORT}/ws/terminal\x1b[0m`);
});
