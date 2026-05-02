import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Folder, Calendar, CheckCircle, Clock } from 'lucide-react'
import api from '../utils/api'
import { useAuth } from '../context/AuthContext'
import { toast } from '../utils/toast'
import { useShortcut } from '../utils/useShortcut'
import { SkeletonGrid } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const STATUS_LABEL = {
  planificacion: 'Planificación',
  en_progreso:   'En progreso',
  pausado:       'Pausado',
  completado:    'Completado',
}
const STATUS_CHIP = {
  planificacion: 'chip-muted',
  en_progreso:   'chip-accent',
  pausado:       'chip-warn',
  completado:    'chip-success',
}

const FILTROS = [
  { label: 'Todos', value: '' },
  { label: 'En progreso', value: 'en_progreso' },
  { label: 'Planificación', value: 'planificacion' },
  { label: 'Pausados', value: 'pausado' },
  { label: 'Completados', value: 'completado' },
]

export default function Dashboard() {
  const { isManager } = useAuth()
  const nav = useNavigate()
  const [proyectos, setProyectos] = useState([])
  const [filtro, setFiltro] = useState('')
  const [openModal, setOpenModal] = useState(false)
  const [loading, setLoading] = useState(true)

  const load = () => {
    api.get('/api/proyectos').then(r => { setProyectos(r.data); setLoading(false) })
  }
  useEffect(() => { load() }, [])

  // Atajo: N para nuevo proyecto (solo manager+)
  useShortcut('n', () => isManager && setOpenModal(true), { enabled: !openModal })

  const filtrados = filtro ? proyectos.filter(p => p.status === filtro) : proyectos

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Optimizar IA</div>
        <div className="flex items-end justify-between flex-wrap gap-4">
          <div>
            <h1 className="hero-title text-5xl md:text-6xl mb-3">Proyectos.</h1>
            <p className="hero-sub">Cada proyecto, un ecosistema completo.</p>
          </div>
          {isManager && (
            <button onClick={() => setOpenModal(true)} className="btn-accent">
              <Plus size={14} /> Nuevo proyecto
            </button>
          )}
        </div>
      </header>

      {/* Filtros */}
      <div className="flex gap-2 mb-8 flex-wrap">
        {FILTROS.map(f => {
          const count = f.value ? proyectos.filter(p => p.status === f.value).length : proyectos.length
          return (
            <button key={f.value}
              onClick={() => setFiltro(f.value)}
              className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
                filtro === f.value
                  ? 'bg-primary text-neutral-50 shadow-soft'
                  : 'bg-white text-muted hover:bg-neutral-200/70 border border-border'
              }`}>
              {f.label} <span className="ml-1 opacity-60">({count})</span>
            </button>
          )
        })}
      </div>

      {loading ? (
        <SkeletonGrid count={6} type="card" />
      ) : filtrados.length === 0 ? (
        <EmptyState
          icon={Folder}
          title={filtro ? 'Sin proyectos en este estado' : 'Todavía no hay proyectos'}
          description={filtro
            ? 'Probá cambiar el filtro o crear un proyecto nuevo.'
            : 'Arrancá creando tu primer proyecto. Tip: presioná "N" para crear rápido.'}
          action={isManager && !filtro ? () => setOpenModal(true) : null}
          actionLabel="+ Crear primer proyecto"
        />
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtrados.map(p => (
            <ProyectoCard key={p.id} proyecto={p} onClick={() => nav(`/proyecto/${p.id}`)} />
          ))}
        </div>
      )}

      {openModal && <ModalNuevoProyecto onClose={() => setOpenModal(false)} onSaved={load} />}
    </div>
  )
}

function ProyectoCard({ proyecto: p, onClick }) {
  const fechaFin = p.fecha_fin ? new Date(p.fecha_fin).toLocaleDateString('es-AR', { day:'2-digit', month:'short', year:'numeric' }) : null
  return (
    <div onClick={onClick}
      className="card p-6 card-hover cursor-pointer group">
      <div className="flex items-start justify-between mb-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl flex items-center justify-center text-white text-sm font-bold"
            style={{ backgroundColor: p.color }}>
            {p.nombre[0]}
          </div>
          <div>
            <div className="font-bold text-[15px] tracking-tight leading-tight group-hover:text-accent transition-colors">
              {p.nombre}
            </div>
            <div className="text-[12px] text-muted mt-0.5">{p.cliente}</div>
          </div>
        </div>
        <span className={STATUS_CHIP[p.status]}>{STATUS_LABEL[p.status]}</span>
      </div>

      {p.descripcion && (
        <p className="text-[13px] text-muted leading-relaxed mb-5 line-clamp-2">{p.descripcion}</p>
      )}

      {/* Progress */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-[11px] uppercase tracking-wider text-muted">Avance</span>
          <span className="font-bold text-[15px] tracking-tight" style={{ color: p.color }}>
            {p.progreso}%
          </span>
        </div>
        <div className="progress-track h-1.5">
          <div className="progress-fill h-full" style={{ width: `${p.progreso}%`, backgroundColor: p.color }} />
        </div>
      </div>

      <div className="flex items-center justify-between text-[12px] text-muted">
        <div className="flex items-center gap-1">
          <CheckCircle size={12} />
          <span>{p.tareas_completadas}/{p.total_tareas} tareas</span>
        </div>
        {fechaFin && (
          <div className="flex items-center gap-1">
            <Calendar size={12} />
            <span>{fechaFin}</span>
          </div>
        )}
      </div>
    </div>
  )
}

function ModalNuevoProyecto({ onClose, onSaved }) {
  const [form, setForm] = useState({
    nombre: '', cliente: '', descripcion: '',
    color: '#6366F1', fecha_inicio: '', fecha_fin: ''
  })
  const [saving, setSaving] = useState(false)
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const COLORES = ['#6366F1','#10B981','#F59E0B','#EF4444','#8B5CF6','#06B6D4','#EC4899','#0EA5E9']

  useShortcut('Escape', onClose)

  const handle = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post('/api/proyectos', {
        ...form,
        fecha_inicio: form.fecha_inicio || null,
        fecha_fin: form.fecha_fin || null,
      })
      toast.success(`Proyecto "${form.nombre}" creado`)
      onSaved()
      onClose()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'No se pudo crear el proyecto')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-primary/30 backdrop-blur-sm z-50 grid place-items-center p-6"
      onClick={onClose}>
      <div className="card p-8 max-w-lg w-full shadow-lift animate-scale-in"
        onClick={e => e.stopPropagation()}>
        <h2 className="hero-title text-2xl mb-6">Nuevo proyecto.</h2>
        <form onSubmit={handle} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className="label">Nombre del proyecto</label>
              <input className="input" required placeholder="Automatización de..." value={form.nombre} onChange={set('nombre')} />
            </div>
            <div className="col-span-2">
              <label className="label">Cliente</label>
              <input className="input" required placeholder="Empresa S.A." value={form.cliente} onChange={set('cliente')} />
            </div>
            <div>
              <label className="label">Fecha inicio</label>
              <input className="input" type="date" value={form.fecha_inicio} onChange={set('fecha_inicio')} />
            </div>
            <div>
              <label className="label">Fecha fin estimada</label>
              <input className="input" type="date" value={form.fecha_fin} onChange={set('fecha_fin')} />
            </div>
            <div className="col-span-2">
              <label className="label">Descripción</label>
              <textarea className="textarea" rows={2} placeholder="Breve descripción..." value={form.descripcion} onChange={set('descripcion')} />
            </div>
            <div className="col-span-2">
              <label className="label">Color del proyecto</label>
              <div className="flex gap-2 flex-wrap">
                {COLORES.map(c => (
                  <button key={c} type="button" onClick={() => setForm(f => ({...f, color: c}))}
                    className={`w-8 h-8 rounded-xl transition-transform ${form.color === c ? 'scale-125 ring-2 ring-offset-2 ring-primary' : 'hover:scale-110'}`}
                    style={{ backgroundColor: c }} />
                ))}
              </div>
            </div>
          </div>
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-accent flex-1 disabled:opacity-50">
              {saving ? 'Creando...' : 'Crear proyecto'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
