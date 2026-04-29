import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { LogOut, Search, Bell, Zap } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import Logo from './Logo'
import api from '../utils/api'

export default function HUD() {
  const { user, logout } = useAuth()
  const nav = useNavigate()
  const [hud, setHud] = useState(null)

  useEffect(() => {
    api.get('/api/dashboard/hud').then(r => setHud(r.data)).catch(() => {})
    const id = setInterval(() => {
      api.get('/api/dashboard/hud').then(r => setHud(r.data)).catch(() => {})
    }, 30000)
    return () => clearInterval(id)
  }, [])

  return (
    <header className="sticky top-0 z-40 glass border-b border-neutral-200 dark:border-slate-700/60 transition-colors duration-200">
      <div className="px-6 h-12 flex items-center gap-6">
        <button onClick={() => nav('/')} className="flex items-center hover:opacity-70 transition">
          <Logo size="sm" />
        </button>

        {hud && (
          <div className="hidden md:flex items-center gap-5 ml-4">
            <Stat label="Proyectos"   value={hud.total_proyectos} />
            <Stat label="Activos"     value={hud.proyectos_activos} accent />
            <Stat label="Tareas"      value={hud.total_tareas} />
            <Stat label="Horas/sem"   value={`${hud.horas_semana}h`} />
            {hud.requerimientos_nuevos > 0 && (
              <button onClick={() => nav('/requerimientos')}
                className="chip-accent animate-pulse cursor-pointer">
                <Zap size={10} />
                {hud.requerimientos_nuevos} nuevo{hud.requerimientos_nuevos > 1 ? 's' : ''}
              </button>
            )}
          </div>
        )}

        <div className="ml-auto flex items-center gap-1">
          <IconBtn><Search size={15} /></IconBtn>
          <IconBtn><Bell size={15} /></IconBtn>
          <div className="w-px h-5 bg-neutral-200 dark:bg-slate-700 mx-2" />
          <button className="flex items-center gap-2 pr-3 pl-1 py-1 rounded-full
                             hover:bg-neutral-200/70 dark:hover:bg-slate-700/60 transition">
            <div className="w-7 h-7 rounded-full bg-accent text-white grid place-items-center text-[11px] font-semibold">
              {user?.nombre?.[0]?.toUpperCase()}
            </div>
            <span className="text-[13px] font-medium hidden md:inline tracking-tight
                             text-primary dark:text-slate-100">
              {user?.nombre}
            </span>
          </button>
          <IconBtn onClick={logout}><LogOut size={15} /></IconBtn>
        </div>
      </div>
    </header>
  )
}

function Stat({ label, value, accent }) {
  return (
    <div className="flex flex-col items-center">
      <span className={`font-semibold text-sm tracking-tight ${accent ? 'text-accent' : 'text-primary dark:text-slate-100'}`}>
        {value}
      </span>
      <span className="text-[9px] uppercase tracking-[0.14em] text-muted dark:text-slate-500">{label}</span>
    </div>
  )
}

function IconBtn({ children, ...props }) {
  return (
    <button {...props}
      className="p-2 rounded-full text-muted hover:bg-neutral-200/70 dark:hover:bg-slate-700/60
                 hover:text-primary dark:hover:text-slate-100 transition">
      {children}
    </button>
  )
}
