import { useEffect, useState } from 'react'
import { Trash2 } from 'lucide-react'
import api from '../utils/api'
import { useAuth } from '../context/AuthContext'

const ROLE_LABEL = { admin:'Admin', manager:'Manager', developer:'Developer', viewer:'Viewer' }
const ROLE_CHIP  = { admin:'chip-danger', manager:'chip-warn', developer:'chip-accent', viewer:'chip-muted' }

export default function Equipo() {
  const { user } = useAuth()
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => api.get('/api/users').then(r => { setUsuarios(r.data); setLoading(false) })
  useEffect(() => { load() }, [])

  const cambiarRol = async (uid, role) => {
    await api.patch(`/api/users/${uid}`, { role })
    load()
  }

  const eliminar = async uid => {
    if (!confirm('¿Eliminar usuario?')) return
    await api.delete(`/api/users/${uid}`)
    load()
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Administración</div>
        <h1 className="hero-title text-5xl md:text-6xl mb-3">Equipo.</h1>
        <p className="hero-sub">Gestioná los miembros y sus roles.</p>
      </header>

      <div className="card overflow-hidden">
        {loading ? (
          <div className="p-8 space-y-4">
            {[1,2,3].map(i => <div key={i} className="h-12 bg-neutral-100 rounded-2xl animate-pulse" />)}
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/60">
                <th className="text-left px-6 py-4 text-[11px] uppercase tracking-wider text-muted font-semibold">Usuario</th>
                <th className="text-left px-6 py-4 text-[11px] uppercase tracking-wider text-muted font-semibold">Email</th>
                <th className="text-left px-6 py-4 text-[11px] uppercase tracking-wider text-muted font-semibold">Rol</th>
                <th className="text-left px-6 py-4 text-[11px] uppercase tracking-wider text-muted font-semibold">Estado</th>
                <th className="px-6 py-4" />
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {usuarios.map(u => (
                <tr key={u.id} className="hover:bg-neutral-50/60 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-accent text-white grid place-items-center text-[12px] font-semibold flex-shrink-0">
                        {u.nombre[0]?.toUpperCase()}
                      </div>
                      <span className="font-medium text-[14px] tracking-tight">{u.nombre}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-[13px] text-muted">{u.email}</td>
                  <td className="px-6 py-4">
                    {u.id === user?.id ? (
                      <span className={ROLE_CHIP[u.role]}>{ROLE_LABEL[u.role]}</span>
                    ) : (
                      <select
                        value={u.role}
                        onChange={e => cambiarRol(u.id, e.target.value)}
                        className="text-[12px] bg-neutral-100 border-0 rounded-xl px-3 py-1.5 font-medium cursor-pointer focus:outline-none focus:ring-2 focus:ring-accent/20">
                        {Object.entries(ROLE_LABEL).map(([v, l]) => (
                          <option key={v} value={v}>{l}</option>
                        ))}
                      </select>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <span className={u.is_active ? 'chip-success' : 'chip-danger'}>
                      {u.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {u.id !== user?.id && (
                      <button onClick={() => eliminar(u.id)}
                        className="text-muted/40 hover:text-danger transition p-1.5 rounded-lg hover:bg-danger/5">
                        <Trash2 size={14} />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="mt-6 card p-5 flex items-center justify-between">
        <div>
          <div className="font-medium text-[14px]">Invitar nuevo miembro</div>
          <div className="text-[12px] text-muted mt-0.5">Compartí el link de registro con el equipo.</div>
        </div>
        <button onClick={() => {
          navigator.clipboard.writeText(window.location.origin + '/register')
          alert('Link copiado al portapapeles')
        }} className="btn-secondary">
          Copiar link de registro
        </button>
      </div>
    </div>
  )
}
