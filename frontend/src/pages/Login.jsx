import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Logo from '../components/Logo'
import { toast } from '../utils/toast'

export default function Login() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handle = async e => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(form.email, form.password)
      toast.success('¡Bienvenido!')
      nav('/')
    } catch {
      setError('Credenciales inválidas. Verificá email y contraseña.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen grid lg:grid-cols-[1.1fr_1fr] bg-bg">
      {/* Izquierda — hero */}
      <div className="hidden lg:flex flex-col justify-between p-14 xl:p-20 bg-primary text-white relative overflow-hidden">
        <div className="absolute -top-40 -left-40 w-[500px] h-[500px] rounded-full bg-accent/20 blur-3xl" />
        <div className="absolute -bottom-40 -right-20 w-[420px] h-[420px] rounded-full bg-accent/10 blur-3xl" />

        <Logo size="md" color="white" tagline />

        <div className="relative z-10 max-w-lg animate-slide-up">
          <div className="text-[12px] uppercase tracking-[0.22em] text-accent-300 font-semibold mb-5">
            Automatización · Eficiencia · Resultados
          </div>
          <h1 className="hero-title text-6xl xl:text-7xl mb-6 text-white">
            Tu equipo.<br />
            <span className="text-accent-300">Un solo lugar.</span>
          </h1>
          <p className="text-white/70 text-lg leading-relaxed font-light max-w-md">
            Gestión de proyectos, seguimiento de tiempo y levantamiento de requerimientos en una plataforma minimalista.
          </p>
        </div>

        <div className="relative z-10">
          <div className="inline-flex items-center gap-3 bg-white/10 rounded-2xl px-4 py-3 border border-white/10">
            <div className="text-[11px] text-white/50 uppercase tracking-wider">Demo</div>
            <div className="w-px h-3 bg-white/20" />
            <code className="text-[12px] text-accent-300">admin@optimizar.com</code>
            <span className="text-white/30">/</span>
            <code className="text-[12px] text-white/70">demo1234</code>
          </div>
        </div>
      </div>

      {/* Derecha — form */}
      <div className="flex flex-col justify-center px-6 py-12 lg:px-20">
        <div className="w-full max-w-sm mx-auto animate-fade-in">
          <div className="lg:hidden mb-10">
            <Logo size="md" />
          </div>
          <h2 className="font-display text-4xl font-bold tracking-[-0.035em] text-primary mb-2">
            Iniciar sesión
          </h2>
          <p className="text-muted text-[15px] font-light mb-10">Bienvenido de vuelta.</p>

          <form onSubmit={handle} className="space-y-5">
            <div>
              <label className="label">Email</label>
              <input className="input" type="email" placeholder="tu@email.com" required
                value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} />
            </div>
            <div>
              <label className="label">Contraseña</label>
              <input className="input" type="password" placeholder="••••••••" required
                value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
            </div>

            {error && (
              <div className="text-danger text-[13px] bg-danger/5 rounded-xl px-4 py-3">{error}</div>
            )}

            <button type="submit" disabled={loading}
              className="btn-primary btn-lg w-full disabled:opacity-50">
              {loading ? 'Ingresando...' : 'Continuar'}
            </button>
          </form>

          <p className="mt-8 text-center text-[13px] text-muted">
            ¿No tenés cuenta?{' '}
            <Link to="/register" className="text-accent-600 font-medium hover:text-accent-700">
              Registrate
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
