import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import {
  LayoutGrid, CheckSquare, FileText, Users,
  Zap, Sun, Moon, Briefcase, Code2,
  ClipboardList, UserCheck, Bell, Keyboard, Kanban, Bot, Megaphone, Package, Rocket
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { useTheme } from '../../context/ThemeContext'
import { useShortcut } from '../../utils/useShortcut'
import KeyboardShortcutsModal from '../KeyboardShortcutsModal'

const link = ({ isActive }) =>
  `flex items-center gap-3 px-3 py-2 rounded-xl text-[13px] font-medium tracking-tight transition-all duration-200 ${
    isActive
      ? 'bg-primary dark:bg-accent text-neutral-50 shadow-soft'
      : 'text-primary/65 dark:text-slate-400 hover:bg-neutral-200/60 dark:hover:bg-slate-700/60 hover:text-primary dark:hover:text-slate-100'
  }`

export default function Sidebar() {
  const { isAdmin, isManager } = useAuth()
  const { dark, toggle } = useTheme()
  const [shortcutsOpen, setShortcutsOpen] = useState(false)

  // Atajo: ? abre el modal de ayuda
  useShortcut(['shift+/', '?'], () => setShortcutsOpen(true))

  return (
    <aside className="w-60 shrink-0 border-r border-neutral-200 dark:border-slate-700/60
                      bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm
                      min-h-[calc(100vh-3rem)] py-5 px-3 flex flex-col transition-colors duration-200">

      {/* ── COMERCIAL ───────────────────────────────────── */}
      <div className="section-label !mt-0 flex items-center gap-1.5">
        <Briefcase size={9} className="text-accent" />
        Comercial
      </div>

      <NavLink to="/crm" className={link}>
        <Kanban size={15} strokeWidth={1.8} />
        CRM · Pipeline
      </NavLink>

      <NavLink to="/contactos" className={link}>
        <Users size={15} strokeWidth={1.8} />
        Contactos
      </NavLink>

      {isManager && (
        <NavLink to="/prospeccion" className={link}>
          <Bot size={15} strokeWidth={1.8} />
          Prospección IA
        </NavLink>
      )}

      <NavLink to="/requerimientos" className={link}>
        <FileText size={15} strokeWidth={1.8} />
        Requerimientos
      </NavLink>

      <NavLink to="/requerimientos/nuevo" className={link}>
        <ClipboardList size={15} strokeWidth={1.8} />
        Cargar Requerimiento
      </NavLink>

      <NavLink to="/servicios" className={link}>
        <Package size={15} strokeWidth={1.8} />
        Nuestros Servicios
      </NavLink>

      {/* ── MARKETING ───────────────────────────────────── */}
      {isManager && (
        <>
          <div className="section-label flex items-center gap-1.5">
            <Megaphone size={9} className="text-accent" />
            Marketing
          </div>
          <NavLink to="/marketing" className={link}>
            <Megaphone size={15} strokeWidth={1.8} />
            Meta Ads
          </NavLink>
          <NavLink to="/agentes" className={link}>
            <Bot size={15} strokeWidth={1.8} />
            Centro de Agentes
          </NavLink>
        </>
      )}

      {/* ── DESARROLLO ──────────────────────────────────── */}
      <div className="section-label flex items-center gap-1.5">
        <Code2 size={9} className="text-accent" />
        Desarrollo
      </div>

      <NavLink to="/" end className={link}>
        <LayoutGrid size={15} strokeWidth={1.8} />
        Proyectos
      </NavLink>

      <NavLink to="/tareas" className={link}>
        <CheckSquare size={15} strokeWidth={1.8} />
        Tareas
      </NavLink>

      {/* ── HERRAMIENTAS ────────────────────────────────── */}
      <div className="section-label flex items-center gap-1.5">
        <Rocket size={9} className="text-accent" />
        Herramientas
      </div>

      <NavLink to="/accesos" className={link}>
        <Rocket size={15} strokeWidth={1.8} />
        Accesos directos
      </NavLink>

      {/* ── ADMINISTRACIÓN ──────────────────────────────── */}
      {isManager && (
        <>
          <div className="section-label flex items-center gap-1.5">
            <UserCheck size={9} className="text-accent" />
            Administración
          </div>

          <NavLink to="/equipo" className={link}>
            <Users size={15} strokeWidth={1.8} />
            Equipo
          </NavLink>
          <NavLink to="/notificaciones" className={link}>
            <Bell size={15} strokeWidth={1.8} />
            Notificaciones
          </NavLink>
        </>
      )}

      {/* ── FOOTER ──────────────────────────────────────── */}
      <div className="mt-auto pt-6 px-1 space-y-2">
        {/* Atajos de teclado */}
        <button
          onClick={() => setShortcutsOpen(true)}
          className="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-xl
                     text-[12px] font-medium tracking-tight transition-all duration-200
                     text-muted dark:text-slate-400
                     hover:bg-neutral-200/60 dark:hover:bg-slate-700/60
                     hover:text-primary dark:hover:text-slate-100">
          <span className="flex items-center gap-2">
            <Keyboard size={13} />
            Atajos
          </span>
          <kbd className="px-1.5 py-0.5 text-[10px] font-mono rounded bg-neutral-200/70 dark:bg-slate-700/60 text-muted">?</kbd>
        </button>

        {/* Toggle tema */}
        <button
          onClick={toggle}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl
                     text-[13px] font-medium tracking-tight transition-all duration-200
                     text-muted dark:text-slate-400
                     hover:bg-neutral-200/60 dark:hover:bg-slate-700/60
                     hover:text-primary dark:hover:text-slate-100 group">
          <div className="relative w-8 h-4 rounded-full transition-all duration-300
                          bg-neutral-300 dark:bg-accent flex items-center px-0.5">
            <div className={`w-3 h-3 rounded-full bg-white shadow-sm transition-all duration-300 ${
              dark ? 'translate-x-4' : 'translate-x-0'
            }`} />
          </div>
          <span className="flex items-center gap-1.5">
            {dark
              ? <><Moon size={12} className="text-accent" /> Modo oscuro</>
              : <><Sun size={12} className="text-warn" /> Modo claro</>
            }
          </span>
        </button>

        {/* Marca */}
        <div className="px-3 pb-1">
          <div className="flex items-center gap-1.5 mb-0.5">
            <Zap size={9} className="text-accent" />
            <span className="text-[10px] tracking-[0.18em] uppercase text-muted/60 dark:text-slate-500 font-semibold">
              Optimizar
            </span>
          </div>
          <div className="text-[10px] text-muted/50 dark:text-slate-600 tracking-wide">
            Automatización · Eficiencia · Resultados
          </div>
        </div>
      </div>

      {shortcutsOpen && <KeyboardShortcutsModal onClose={() => setShortcutsOpen(false)} />}
    </aside>
  )
}
