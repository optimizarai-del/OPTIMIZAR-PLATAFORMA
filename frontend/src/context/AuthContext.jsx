import { createContext, useContext, useEffect, useState } from 'react'
import api from '../utils/api'

const AuthContext = createContext()
export const useAuth = () => useContext(AuthContext)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    const token = localStorage.getItem('opt_token')
    if (token) {
      api.get('/auth/me')
        .then(r => { if (alive) setUser(r.data) })
        .catch(() => localStorage.removeItem('opt_token'))
        .finally(() => { if (alive) setLoading(false) })
    } else {
      setLoading(false)
    }
    return () => { alive = false }
  }, [])

  const login = async (email, password) => {
    const r = await api.post('/auth/login', { email, password })
    localStorage.setItem('opt_token', r.data.access_token)
    setUser(r.data.user)
  }

  const logout = () => {
    localStorage.removeItem('opt_token')
    setUser(null)
    window.location.href = '/login'
  }

  const isAdmin    = user?.role === 'admin'
  const isManager  = user?.role === 'admin' || user?.role === 'manager'

  return (
    <AuthContext.Provider value={{ user, login, logout, loading, isAdmin, isManager }}>
      {children}
    </AuthContext.Provider>
  )
}
