import { NavLink } from 'react-router-dom'
import { LayoutGrid, CheckSquare, FileText, Users, Zap } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import Logo from '../Logo'

const link = ({ isActive }) =>
  `flex items-center gap-3 px-3 py-2 rounded-xl text-[13px] font-medium tracking-tight transition-all duration-200 ${
    isActive
      ? 'bg-primary text-neutral-50 shadow-soft'
      : 'text-primary/65 hover:bg-neutral-200/60 hover:text-primary'
  }`

export default function Sidebar() {
  const { isManager } = useAuth()

  return (
    <aside className="w-60 shrink-0 border-r border-border/60 bg-white/30 backdrop-blur-sm
                      min-h-[calc(100vh-3rem)] py-5 px-3 flex flex-col">
      <div className="section-label !mt-0">General</div>
      <NavLink to="/" end className={link}>
        <LayoutGrid size={15} strokeWidth={1.8} /> Dashboard
      </NavLink>
      <NavLink to="/tareas" className={link}>
        <CheckSquare size={15} strokeWidth={1.8} /> Tareas
      </NavLink>

      <div className="section-label">Comercial</div>
      <NavLink to="/requerimientos" className={link}>
        <FileText size={15} strokeWidth={1.8} /> Requerimientos
      </NavLink>

      {isManager && (
        <>
          <div className="section-label">Administración</div>
          <NavLink to="/equipo" className={link}>
            <Users size={15} strokeWidth={1.8} /> Equipo
          </NavLink>
        </>
      )}

      <div className="mt-auto pt-6 px-3">
        <div className="flex items-center gap-1.5 mb-1">
          <Zap size={10} className="text-accent" />
          <div className="text-[10px] tracking-[0.18em] uppercase text-muted/60 font-semibold">Optimizar</div>
        </div>
        <div className="text-[10px] text-muted/50 tracking-wide">Automatización · Eficiencia · Resultados</div>
      </div>
    </aside>
  )
}
