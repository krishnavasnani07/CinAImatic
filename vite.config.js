import { resolve } from 'path';
import { defineConfig } from 'vite';
import { readdirSync } from 'fs';

const screensDir = resolve(__dirname, 'screens');
const screenFiles = readdirSync(screensDir).filter(file => file.endsWith('.html'));

const inputs = {
  main: resolve(__dirname, 'index.html'),
};

screenFiles.forEach(file => {
  const name = file.replace('.html', '');
  inputs[name] = resolve(__dirname, `screens/${file}`);
});

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8001',
        ws: true,
      },
    },
  },
  build: {
    rollupOptions: {
      input: inputs,
    },
  },
});
