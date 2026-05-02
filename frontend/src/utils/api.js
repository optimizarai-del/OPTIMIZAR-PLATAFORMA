import axios from 'axios'
import { toast } from './toast'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8765' })

api.interceptors.request.use(config => {
  // Token JWT
  const token = localStorage.getItem('opt_token')
  if (token) config.headers.Authorization = `Bearer ${token}`

  // Normalizar trailing slash SOLO en endpoints de coleccion root tipo
  // /api/proyectos, /api/tareas, etc. — esos son los unicos que FastAPI
  // declara con `route="/"` y necesitan el slash final.
  // No tocar /api/proyectos/4, /api/proyectos/4/plan, /api/notificaciones/stats
  // porque esos son endpoints que NO tienen slash al final en FastAPI y
  // agregarlo da 404.
  if (config.url) {
    const [path, qs] = config.url.split('?')
    if (/^\/api\/[a-z_-]+$/i.test(path)) {
      config.url = path + '/' + (qs ? '?' + qs : '')
    }
  }
  return config
})

api.interceptors.response.use(r => r, err => {
  if (err.response?.status === 401) {
    // Solo redirige si NO estamos en /login (evita loop al fallar el propio login)
    if (!window.location.pathname.startsWith('/login')) {
      localStorage.removeItem('opt_token')
      window.location.href = '/login'
    }
  } else if (err.response?.status >= 500) {
    toast.error('Error del servidor. Probá de nuevo.')
  } else if (!err.response) {
    // Error de red (sin internet, backend caido)
    toast.error('Sin conexión con el servidor.')
  }
  return Promise.reject(err)
})

export default api
