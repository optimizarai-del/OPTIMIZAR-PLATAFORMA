import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5800,         // exclusivo de Optimizar (evita colisión con CIUDAD/otros en 5173)
    strictPort: true,   // si está ocupado, falla en vez de saltar a otro
    host: 'localhost',
  },
})
