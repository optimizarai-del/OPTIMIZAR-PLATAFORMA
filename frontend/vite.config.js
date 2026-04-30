import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// El server config solo afecta `vite dev`. En produccion (`vite build` + nginx)
// se ignora completamente.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5800,         // exclusivo de Optimizar (evita colisión con otros locales)
    strictPort: true,   // si está ocupado, falla en vez de saltar a otro
    host: 'localhost',
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
