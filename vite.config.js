import { resolve } from 'path';
import { defineConfig } from 'vite';
import { readdirSync } from 'fs';
import react from '@vitejs/plugin-react';

const screensDir = resolve(__dirname, 'screens');
let screenFiles = [];
try {
  screenFiles = readdirSync(screensDir).filter(file => file.endsWith('.html'));
} catch (e) {
  // directory might not exist yet
}

const inputs = {
  main: resolve(__dirname, 'index.html'),
};

screenFiles.forEach(file => {
  const name = file.replace('.html', '');
  inputs[name] = resolve(__dirname, `screens/${file}`);
});

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: inputs,
    },
  },
});
