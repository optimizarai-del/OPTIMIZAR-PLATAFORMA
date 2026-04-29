import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Logo from '../components/Logo'
import api from '../utils/api'

export default function Register() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [form, setForm] = useState({ nombre: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handle = async e => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const r = await api.post('/auth/register', { ...form, role: 'developer' })
      localStorage.setItem('opt_token', r.data.access_token)
      window.location.href = '/'
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrarse')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-bg flex flex-col justify-center px-6 py-12">
      <div className="w-full max-w-md mx-auto animate-fade-in">
        <div className="mb-10 text-center">
          <Logo size="md" className="mx-auto mb-6" />
          <h2 className="font-display text-4xl font-bold tracking-[-0.035em] text-primary mb-2">
            Crear cuenta
          </h2>
          <p className="text-muted text-[15px] font-light">Unite al equipo de Optimizar.</p>
        </div>

        <div className="card p-8 shadow-card">
          <form onSubmit={handle} className="space-y-5">
            <div>
              <label className="label">Nombre completo</label>
              <input className="input" placeholder="Juan Pérez" required
                value={form.nombre} onChange={set('nombre')} />
            </div>
            <div>
              <label className="label">Email</label>
              <input className="input" type="email" placeholder="tu@email.com" required
                value={form.email} onChange={set('email')} />
            </div>
            <div>
              <label className="label">Contraseña</label>
              <input className="input" type="password" placeholder="Mínimo 8 caracteres" required minLength={6}
                value={form.password} onChange={set('password')} />
            </div>

            {error && (
              <div className="text-danger text-[13px] bg-danger/5 rounded-xl px-4 py-3">{error}</div>
            )}

            <button type="submit" disabled={loading} className="btn-primary btn-lg w-full disabled:opacity-50">
              {loading ? 'Creando cuenta...' : 'Crear cuenta'}
            </button>
          </form>
        </div>

        <p className="mt-6 text-center text-[13px] text-muted">
          ¿Ya tenés cuenta?{' '}
          <Link to="/login" className="text-accent-600 font-medium hover:text-accent-700">
            Iniciá sesión
          </Link>
        </p>
      </div>
    </div>
  )
}
