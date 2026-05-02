import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8765' })

api.interceptors.request.use(config => {
  // Token JWT
  const token = localStorage.getItem('opt_token')
  if (token) config.headers.Authorization = `Bearer ${token}`

  // Normalizar trailing slash en endpoints de coleccion para evitar el 307
  // de FastAPI. Como back y front estan en subdominios distintos (cross-origin),
  // Chrome dropea Authorization en redirects → la 2da request falla con 401.
  // Solo aplico al PATH (sin querystring), y no toco URLs que ya tienen extension
  // (.json, .pdf, etc) ni paths que ya terminan en slash.
  if (config.url && config.url.startsWith('/api/')) {
    const [path, qs] = config.url.split('?')
    if (!path.endsWith('/') && !/\.[a-z0-9]+$/i.test(path)) {
      config.url = path + '/' + (qs ? '?' + qs : '')
    }
  }
  return config
})

api.interceptors.response.use(r => r, err => {
  if (err.response?.status === 401) {
    localStorage.removeItem('opt_token')
    window.location.href = '/login'
  }
  return Promise.reject(err)
})

export default api
