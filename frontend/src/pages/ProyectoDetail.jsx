import { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Plus, Check, Clock, ChevronRight, Trash2, Play, Square, Timer,
         Github, RefreshCw, CheckCircle, GitCommit, Zap, Link, Unlink } from 'lucide-react'
import api from '../utils/api'
import { useAuth } from '../context/AuthContext'

const STATUS_OPTIONS = ['pendiente','en_progreso','revision','completada','bloqueada']
const STATUS_LABEL   = { pendiente:'Pendiente', en_progreso:'En progreso', revision:'Revisión', completada:'Completada', bloqueada:'Bloqueada' }
const STATUS_CHIP    = { pendiente:'chip-muted', en_progreso:'chip-accent', revision:'chip-warn', completada:'chip-success', bloqueada:'chip-danger' }
const PRIO_CHIP      = { baja:'chip-muted', media:'chip-primary', alta:'chip-warn', urgente:'chip-danger' }
const PRIO_LABEL     = { baja:'Baja', media:'Media', alta:'Alta', urgente:'Urgente' }
const PROJ_STATUS    = { planificacion:'Planificación', en_progreso:'En progreso', pausado:'Pausado', completado:'Completado' }

const TABS = ['Resumen','Tareas','Plan de Acción','GitHub']

export default function ProyectoDetail() {
  const { id } = useParams()
  const nav = useNavigate()
  const { isManager } = useAuth()
  const [proyecto, setProyecto] = useState(null)
  const [tareas, setTareas] = useState([])
  const [plan, setPlan] = useState([])
  const [tab, setTab] = useState('Resumen')
  const [openTarea, setOpenTarea] = useState(null)
  const [modalTarea, setModalTarea] = useState(false)
  const [modalPunto, setModalPunto] = useState(false)
  const [loading, setLoading] = useState(true)

  const loadAll = useCallback(() => {
    Promise.all([
      api.get(`/api/proyectos/${id}`),
      api.get(`/api/tareas?proyecto_id=${id}`),
      api.get(`/api/proyectos/${id}/plan`),
    ]).then(([p, t, pl]) => {
      setProyecto(p.data)
      setTareas(t.data)
      setPlan(pl.data)
      setLoading(false)
    })
  }, [id])

  useEffect(() => { loadAll() }, [loadAll])

  const togglePunto = async (punto) => {
    await api.patch(`/api/proyectos/${id}/plan/${punto.id}`, { completado: !punto.completado })
    loadAll()
  }

  if (loading) return (
    <div className="min-h-screen grid place-items-center">
      <div className="w-6 h-6 rounded-full border-2 border-accent border-t-transparent animate-spin" />
    </div>
  )
  if (!proyecto) return null

  const fechaFin = proyecto.fecha_fin ? new Date(proyecto.fecha_fin).toLocaleDateString('es-AR', {day:'2-digit',month:'short',year:'numeric'}) : '—'

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-10 pt-8 pb-6 border-b border-border/60 bg-white/50">
        <button onClick={() => nav('/')} className="btn-ghost mb-4 -ml-2 text-muted">
          <ArrowLeft size={14} /> Proyectos
        </button>
        <div className="flex items-start gap-5 flex-wrap">
          <div className="w-14 h-14 rounded-2xl flex items-center justify-center text-white text-xl font-bold shadow-card"
            style={{ backgroundColor: proyecto.color }}>
            {proyecto.nombre[0]}
          </div>
          <div className="flex-1 min-w-0">
            <div className="hero-eyebrow">{proyecto.cliente}</div>
            <h1 className="hero-title text-4xl md:text-5xl mb-2">{proyecto.nombre}.</h1>
            {proyecto.descripcion && (
              <p className="text-muted text-[15px] font-light max-w-2xl">{proyecto.descripcion}</p>
            )}
          </div>
          <div className="flex flex-col items-end gap-2">
            <span className={STATUS_CHIP[proyecto.status] ?? 'chip-muted'}>{PROJ_STATUS[proyecto.status]}</span>
            <span className="text-[12px] text-muted">Entrega: {fechaFin}</span>
          </div>
        </div>

        {/* Mega progress */}
        <div className="mt-6 max-w-2xl">
          <div className="flex justify-between items-center mb-2">
            <span className="text-[11px] uppercase tracking-wider text-muted">Progreso general</span>
            <span className="font-bold text-2xl tracking-tight" style={{ color: proyecto.color }}>
              {proyecto.progreso}%
            </span>
          </div>
          <div className="progress-track h-2">
            <div className="progress-fill h-full" style={{ width: `${proyecto.progreso}%`, backgroundColor: proyecto.color }} />
          </div>
          <div className="flex gap-6 mt-3 text-[12px] text-muted">
            <span><b className="text-primary">{proyecto.tareas_completadas}</b>/{proyecto.total_tareas} tareas</span>
            <span><b className="text-primary">{proyecto.puntos_completados}</b>/{proyecto.total_puntos} puntos de acción</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mt-6">
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-xl text-[13px] font-medium transition-all ${
                tab === t ? 'bg-primary text-white shadow-soft' : 'text-muted hover:bg-neutral-200/70'
              }`}>{t}</button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="px-10 py-8">
        {tab === 'Resumen' && (
          <div className="grid md:grid-cols-3 gap-5 max-w-4xl">
            <StatCard label="Total tareas" value={proyecto.total_tareas} color={proyecto.color} />
            <StatCard label="Completadas" value={proyecto.tareas_completadas} color="#059669" />
            <StatCard label="Puntos de acción" value={`${proyecto.puntos_completados}/${proyecto.total_puntos}`} color={proyecto.color} />
          </div>
        )}

        {tab === 'Tareas' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold tracking-tight">Tareas del proyecto</h2>
              <button onClick={() => setModalTarea(true)} className="btn-accent">
                <Plus size={14} /> Nueva tarea
              </button>
            </div>
            {tareas.length === 0 ? (
              <div className="card py-16 text-center">
                <p className="text-muted">No hay tareas todavía.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {tareas.map(t => (
                  <TareaRow key={t.id} tarea={t} color={proyecto.color}
                    onClick={() => setOpenTarea(t)} onRefresh={loadAll} />
                ))}
              </div>
            )}
          </div>
        )}

        {tab === 'Plan de Acción' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold tracking-tight">Plan de Acción</h2>
              <button onClick={() => setModalPunto(true)} className="btn-accent">
                <Plus size={14} /> Agregar punto
              </button>
            </div>
            {plan.length === 0 ? (
              <div className="card py-16 text-center">
                <p className="text-muted">El plan de acción está vacío.</p>
              </div>
            ) : (
              <div className="space-y-2 max-w-2xl">
                {plan.map((punto, i) => (
                  <div key={punto.id}
                    className={`card p-4 flex items-start gap-4 transition-all ${punto.completado ? 'opacity-60' : ''}`}>
                    <button onClick={() => togglePunto(punto)}
                      className={`mt-0.5 w-6 h-6 rounded-lg border-2 flex items-center justify-center flex-shrink-0 transition-all ${
                        punto.completado ? 'border-success bg-success text-white' : 'border-border hover:border-accent'
                      }`}>
                      {punto.completado && <Check size={12} />}
                    </button>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-[11px] text-muted font-medium">#{i + 1}</span>
                        <span className={`font-medium text-[15px] ${punto.completado ? 'line-through text-muted' : ''}`}>
                          {punto.titulo}
                        </span>
                      </div>
                      {punto.descripcion && (
                        <p className="text-[13px] text-muted mt-1">{punto.descripcion}</p>
                      )}
                    </div>
                    <button onClick={async () => {
                      await api.delete(`/api/proyectos/${id}/plan/${punto.id}`)
                      loadAll()
                    }} className="text-muted/40 hover:text-danger transition p-1">
                      <Trash2 size={13} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {tab === 'GitHub' && (
          <GitHubPanel proyecto={proyecto} onRefresh={loadAll} />
        )}
      </div>

      {modalTarea && (
        <ModalNuevaTarea proyectoId={parseInt(id)} onClose={() => setModalTarea(false)} onSaved={loadAll} />
      )}
      {modalPunto && (
        <ModalNuevoPunto proyectoId={parseInt(id)} onClose={() => setModalPunto(false)} onSaved={loadAll} orden={plan.length} />
      )}
      {openTarea && (
        <TareaDrawer tarea={openTarea} onClose={() => setOpenTarea(null)} onSaved={loadAll} />
      )}
    </div>
  )
}

function StatCard({ label, value, color }) {
  return (
    <div className="card p-6">
      <div className="stat-label mb-2">{label}</div>
      <div className="hero-title text-4xl" style={{ color }}>{value}</div>
    </div>
  )
}

function TareaRow({ tarea: t, color, onClick, onRefresh }) {
  const cambiarStatus = async (e, status) => {
    e.stopPropagation()
    await api.patch(`/api/tareas/${t.id}`, { status })
    onRefresh()
  }
  const horas = Math.floor(t.minutos_trabajados / 60)
  const mins  = t.minutos_trabajados % 60

  return (
    <div onClick={onClick}
      className="card p-4 flex items-center gap-4 card-hover cursor-pointer group">
      <button onClick={e => cambiarStatus(e, t.status === 'completada' ? 'pendiente' : 'completada')}
        className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center flex-shrink-0 transition-all ${
          t.status === 'completada' ? 'border-success bg-success text-white' : 'border-border hover:border-accent'
        }`}>
        {t.status === 'completada' && <Check size={12} />}
      </button>

      <div className="flex-1 min-w-0">
        <div className={`font-medium text-[14px] tracking-tight ${t.status === 'completada' ? 'line-through text-muted' : ''}`}>
          {t.titulo}
        </div>
        <div className="flex items-center gap-3 mt-1">
          <span className={PRIO_CHIP[t.prioridad]}>{PRIO_LABEL[t.prioridad]}</span>
          <span className={STATUS_CHIP[t.status]}>{STATUS_LABEL[t.status]}</span>
          {t.asignado_nombre && <span className="text-[11px] text-muted">{t.asignado_nombre}</span>}
        </div>
      </div>

      <div className="flex items-center gap-4 text-[12px] text-muted flex-shrink-0">
        {t.minutos_trabajados > 0 && (
          <div className="flex items-center gap-1">
            <Clock size={12} />
            <span>{horas > 0 ? `${horas}h ` : ''}{mins}m</span>
          </div>
        )}
        {t.fecha_fin_estimada && (
          <span>{new Date(t.fecha_fin_estimada).toLocaleDateString('es-AR',{day:'2-digit',month:'short'})}</span>
        )}
        <ChevronRight size={14} className="opacity-40 group-hover:opacity-100 transition" />
      </div>
    </div>
  )
}

function TareaDrawer({ tarea: initial, onClose, onSaved }) {
  const { user } = useAuth()
  const [tarea, setTarea] = useState(initial)
  const [registros, setRegistros] = useState([])
  const [timer, setTimer] = useState(null)
  const [seconds, setSeconds] = useState(0)
  const [modalTiempo, setModalTiempo] = useState(false)

  const loadRegistros = () => api.get(`/api/tiempo?tarea_id=${tarea.id}`).then(r => setRegistros(r.data))
  const reloadTarea = () => api.get(`/api/tareas/${tarea.id}`).then(r => setTarea(r.data))

  useEffect(() => { loadRegistros() }, [tarea.id])

  useEffect(() => {
    if (timer) {
      const id = setInterval(() => setSeconds(s => s + 1), 1000)
      return () => clearInterval(id)
    }
  }, [timer])

  const startTimer = () => { setTimer(Date.now()); setSeconds(0) }
  const stopTimer  = async () => {
    if (!timer) return
    const minutos = Math.max(1, Math.round(seconds / 60))
    setTimer(null)
    setSeconds(0)
    await api.post('/api/tiempo', {
      tarea_id: tarea.id, minutos, tipo: 'timer',
      fecha: new Date().toISOString().split('T')[0],
      descripcion: 'Sesión de trabajo (timer)',
    })
    loadRegistros()
    reloadTarea()
    onSaved()
  }

  const cambiarStatus = async status => {
    await api.patch(`/api/tareas/${tarea.id}`, { status })
    reloadTarea()
    onSaved()
  }

  const fmt = s => `${String(Math.floor(s/3600)).padStart(2,'0')}:${String(Math.floor((s%3600)/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`
  const totalHoras = (registros.reduce((a,r) => a + r.minutos, 0) / 60).toFixed(1)

  return (
    <div className="fixed inset-0 bg-primary/20 backdrop-blur-sm z-50 flex justify-end"
      onClick={onClose}>
      <div className="w-full max-w-lg bg-white h-full shadow-lift overflow-y-auto animate-slide-up"
        onClick={e => e.stopPropagation()}>
        <div className="p-6 border-b border-border/60">
          <div className="flex items-start justify-between gap-4 mb-4">
            <h2 className="font-bold text-lg tracking-tight leading-tight">{tarea.titulo}</h2>
            <button onClick={onClose} className="text-muted hover:text-primary transition text-lg leading-none">×</button>
          </div>
          <div className="flex gap-2 flex-wrap">
            <span className={STATUS_CHIP[tarea.status]}>{STATUS_LABEL[tarea.status]}</span>
            <span className={PRIO_CHIP[tarea.prioridad]}>{PRIO_LABEL[tarea.prioridad]}</span>
            {tarea.asignado_nombre && <span className="chip-muted">{tarea.asignado_nombre}</span>}
          </div>
          {tarea.descripcion && (
            <p className="text-[13px] text-muted mt-3 leading-relaxed">{tarea.descripcion}</p>
          )}
          <div className="flex gap-4 mt-4 text-[12px] text-muted">
            {tarea.fecha_inicio && <span>Inicio: {new Date(tarea.fecha_inicio).toLocaleDateString('es-AR')}</span>}
            {tarea.fecha_fin_estimada && <span>Estimada: {new Date(tarea.fecha_fin_estimada).toLocaleDateString('es-AR')}</span>}
          </div>
        </div>

        {/* Cambiar estado */}
        <div className="p-6 border-b border-border/60">
          <label className="label mb-3">Estado</label>
          <div className="flex gap-2 flex-wrap">
            {STATUS_OPTIONS.map(s => (
              <button key={s} onClick={() => cambiarStatus(s)}
                className={`px-3 py-1.5 rounded-full text-[12px] font-medium transition-all ${
                  tarea.status === s ? 'bg-primary text-white shadow-soft' : 'bg-neutral-100 text-muted hover:bg-neutral-200'
                }`}>{STATUS_LABEL[s]}</button>
            ))}
          </div>
        </div>

        {/* Timer */}
        <div className="p-6 border-b border-border/60">
          <div className="flex items-center justify-between mb-4">
            <div>
              <label className="label">Tiempo registrado</label>
              <div className="font-bold text-2xl tracking-tight text-primary">{totalHoras}h total</div>
            </div>
            <button onClick={() => setModalTiempo(true)} className="btn-secondary">
              <Plus size={13} /> Manual
            </button>
          </div>

          {timer ? (
            <div className="flex items-center gap-4 p-4 bg-danger/5 rounded-2xl border border-danger/20">
              <div className="w-3 h-3 rounded-full bg-danger animate-pulse" />
              <span className="font-mono text-xl font-bold text-danger">{fmt(seconds)}</span>
              <button onClick={stopTimer} className="btn-danger ml-auto">
                <Square size={13} /> Detener
              </button>
            </div>
          ) : (
            <button onClick={startTimer} className="btn-accent w-full">
              <Play size={14} /> Iniciar timer
            </button>
          )}

          {registros.length > 0 && (
            <div className="mt-4 space-y-2">
              {registros.slice(0, 5).map(r => (
                <div key={r.id} className="flex items-start gap-3 text-[13px]">
                  <div className="flex items-center gap-1 text-muted flex-shrink-0 mt-0.5">
                    <Timer size={11} />
                    <span className="font-medium text-primary">{r.minutos}m</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-muted">{r.descripcion || '—'}</span>
                    {r.resultado && <div className="text-[12px] text-accent-600 mt-0.5">→ {r.resultado}</div>}
                  </div>
                  <span className="text-muted/60 flex-shrink-0">{new Date(r.fecha).toLocaleDateString('es-AR',{day:'2-digit',month:'short'})}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {modalTiempo && (
        <ModalRegistroManual tareaId={tarea.id} onClose={() => setModalTiempo(false)}
          onSaved={() => { loadRegistros(); reloadTarea(); onSaved() }} />
      )}
    </div>
  )
}

function ModalRegistroManual({ tareaId, onClose, onSaved }) {
  const [form, setForm] = useState({
    minutos: '', descripcion: '', resultado: '',
    fecha: new Date().toISOString().split('T')[0]
  })
  const [saving, setSaving] = useState(false)
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handle = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post('/api/tiempo', { ...form, minutos: parseInt(form.minutos), tarea_id: tareaId, tipo: 'manual' })
      onSaved()
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-primary/30 backdrop-blur-sm z-[60] grid place-items-center p-6"
      onClick={onClose}>
      <div className="card p-7 max-w-md w-full shadow-lift animate-scale-in" onClick={e => e.stopPropagation()}>
        <h3 className="hero-title text-xl mb-5">Cargar tiempo manual.</h3>
        <form onSubmit={handle} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Minutos trabajados</label>
              <input className="input" type="number" min="1" required placeholder="90" value={form.minutos} onChange={set('minutos')} />
            </div>
            <div>
              <label className="label">Fecha</label>
              <input className="input" type="date" required value={form.fecha} onChange={set('fecha')} />
            </div>
          </div>
          <div>
            <label className="label">Descripción (opcional)</label>
            <input className="input" placeholder="¿En qué trabajaste?" value={form.descripcion} onChange={set('descripcion')} />
          </div>
          <div>
            <label className="label">Resultado obtenido (opcional)</label>
            <textarea className="textarea" rows={2} placeholder="¿Qué lograste?" value={form.resultado} onChange={set('resultado')} />
          </div>
          <div className="flex gap-3 pt-1">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-accent flex-1 disabled:opacity-50">
              {saving ? 'Guardando...' : 'Guardar tiempo'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

function ModalNuevaTarea({ proyectoId, onClose, onSaved }) {
  const [form, setForm] = useState({
    titulo: '', descripcion: '', prioridad: 'media',
    fecha_inicio: '', fecha_fin_estimada: '', minutos_estimados: ''
  })
  const [saving, setSaving] = useState(false)
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handle = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post('/api/tareas', {
        ...form, proyecto_id: proyectoId,
        fecha_inicio: form.fecha_inicio || null,
        fecha_fin_estimada: form.fecha_fin_estimada || null,
        minutos_estimados: form.minutos_estimados ? parseInt(form.minutos_estimados) : null,
      })
      onSaved()
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-primary/30 backdrop-blur-sm z-50 grid place-items-center p-6"
      onClick={onClose}>
      <div className="card p-8 max-w-lg w-full shadow-lift animate-scale-in" onClick={e => e.stopPropagation()}>
        <h2 className="hero-title text-2xl mb-6">Nueva tarea.</h2>
        <form onSubmit={handle} className="space-y-4">
          <div>
            <label className="label">Título</label>
            <input className="input" required placeholder="Implementar módulo de..." value={form.titulo} onChange={set('titulo')} />
          </div>
          <div>
            <label className="label">Descripción</label>
            <textarea className="textarea" rows={2} placeholder="Detalles..." value={form.descripcion} onChange={set('descripcion')} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Prioridad</label>
              <select className="input" value={form.prioridad} onChange={set('prioridad')}>
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
                <option value="urgente">Urgente</option>
              </select>
            </div>
            <div>
              <label className="label">Estimado (minutos)</label>
              <input className="input" type="number" min="1" placeholder="120" value={form.minutos_estimados} onChange={set('minutos_estimados')} />
            </div>
            <div>
              <label className="label">Fecha inicio</label>
              <input className="input" type="date" value={form.fecha_inicio} onChange={set('fecha_inicio')} />
            </div>
            <div>
              <label className="label">Fecha fin estimada</label>
              <input className="input" type="date" value={form.fecha_fin_estimada} onChange={set('fecha_fin_estimada')} />
            </div>
          </div>
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-accent flex-1 disabled:opacity-50">
              {saving ? 'Creando...' : 'Crear tarea'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

function GitHubPanel({ proyecto, onRefresh }) {
  const [repo, setRepo]           = useState(proyecto.github_repo || '')
  const [commits, setCommits]     = useState([])
  const [syncing, setSyncing]     = useState(false)
  const [saving, setSaving]       = useState(false)
  const [loadingCommits, setLoadingCommits] = useState(false)
  const [result, setResult]       = useState(null)
  const [error, setError]         = useState(null)

  const loadCommits = async () => {
    if (!proyecto.github_repo) return
    setLoadingCommits(true)
    try {
      const r = await api.get(`/api/proyectos/${proyecto.id}/github/commits`)
      setCommits(r.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Error al cargar commits')
    } finally {
      setLoadingCommits(false)
    }
  }

  useEffect(() => { loadCommits() }, [proyecto.github_repo])

  const saveRepo = async () => {
    setSaving(true)
    setError(null)
    try {
      await api.put(`/api/proyectos/${proyecto.id}/github/repo`, { repo: repo.trim() })
      onRefresh()
      if (repo.trim()) setTimeout(loadCommits, 300)
    } catch (e) {
      setError(e.response?.data?.detail || 'Error al guardar repositorio')
    } finally {
      setSaving(false)
    }
  }

  const sync = async () => {
    setSyncing(true)
    setError(null)
    setResult(null)
    try {
      const r = await api.post(`/api/proyectos/${proyecto.id}/github/sync`)
      setResult(r.data)
      onRefresh()
    } catch (e) {
      setError(e.response?.data?.detail || 'Error al sincronizar')
    } finally {
      setSyncing(false)
    }
  }

  const lastSync = proyecto.github_last_sync
    ? new Date(proyecto.github_last_sync).toLocaleString('es-AR', {day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'})
    : null

  return (
    <div className="max-w-3xl space-y-6">

      {/* Repo config */}
      <div className="card p-6">
        <div className="flex items-center gap-2 mb-4">
          <Github size={16} className="text-primary dark:text-slate-200" />
          <h3 className="font-semibold text-[15px]">Repositorio GitHub</h3>
        </div>
        <div className="flex gap-3">
          <input
            className="input flex-1"
            placeholder="owner/repository  (ej: tu-usuario/mi-proyecto)"
            value={repo}
            onChange={e => setRepo(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && saveRepo()}
          />
          <button onClick={saveRepo} disabled={saving}
            className="btn-accent disabled:opacity-50 flex-shrink-0">
            {saving ? <RefreshCw size={13} className="animate-spin" /> : <Link size={13} />}
            {saving ? 'Verificando...' : 'Vincular'}
          </button>
          {proyecto.github_repo && (
            <button onClick={() => { setRepo(''); saveRepo() }}
              className="btn-ghost text-danger flex-shrink-0">
              <Unlink size={13} />
            </button>
          )}
        </div>
        <p className="text-[11px] text-muted mt-2">
          Ingresá el repositorio en formato <code className="bg-neutral-100 dark:bg-slate-700 px-1 rounded">owner/repo</code>.
          Para repositorios privados configurá <code className="bg-neutral-100 dark:bg-slate-700 px-1 rounded">GITHUB_TOKEN</code> en backend/.env.
        </p>
        {error && (
          <div className="mt-3 p-3 bg-danger/5 rounded-xl border border-danger/20 text-[12px] text-danger">{error}</div>
        )}
      </div>

      {/* Sync panel — only shown when repo is linked */}
      {proyecto.github_repo && (
        <>
          {/* Sync action */}
          <div className="card p-6">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Zap size={14} className="text-accent" />
                  <h3 className="font-semibold text-[15px]">Análisis con IA</h3>
                </div>
                <p className="text-[12px] text-muted">
                  Claude analiza los commits y actualiza automáticamente las tareas y el plan de acción.
                </p>
                {lastSync && (
                  <p className="text-[11px] text-muted/60 mt-1">
                    Última sincronización: {lastSync}
                    {proyecto.github_last_commit_sha && ` · commit ${proyecto.github_last_commit_sha}`}
                  </p>
                )}
              </div>
              <button onClick={sync} disabled={syncing}
                className="btn-accent disabled:opacity-50">
                {syncing
                  ? <><RefreshCw size={13} className="animate-spin" /> Analizando...</>
                  : <><Zap size={13} /> Sincronizar con IA</>
                }
              </button>
            </div>

            {/* Result */}
            {result && (
              <div className="mt-5 space-y-3">
                <div className="p-4 bg-accent/5 dark:bg-accent/10 rounded-xl border border-accent/20">
                  <div className="text-[11px] uppercase tracking-wider text-accent font-semibold mb-2">
                    Resultado del análisis · {result.commits_analizados} commits revisados
                  </div>
                  <p className="text-[13px] text-primary dark:text-slate-200">{result.summary}</p>
                </div>

                {result.task_updates.length > 0 && (
                  <div>
                    <div className="text-[11px] uppercase tracking-wider text-muted mb-2">Tareas actualizadas</div>
                    <div className="space-y-2">
                      {result.task_updates.map((u, i) => (
                        <div key={i} className="flex items-start gap-3 p-3 bg-success/5 rounded-xl border border-success/20">
                          <CheckCircle size={14} className="text-success mt-0.5 flex-shrink-0" />
                          <div>
                            <span className="text-[13px] font-medium">Tarea #{u.id}</span>
                            <span className="text-[12px] text-muted ml-2">→ {u.status}</span>
                            {u.reason && <p className="text-[11px] text-muted mt-0.5">{u.reason}</p>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {result.plan_updates.length > 0 && (
                  <div>
                    <div className="text-[11px] uppercase tracking-wider text-muted mb-2">Plan de acción actualizado</div>
                    <div className="space-y-2">
                      {result.plan_updates.map((u, i) => (
                        <div key={i} className="flex items-start gap-3 p-3 bg-success/5 rounded-xl border border-success/20">
                          <CheckCircle size={14} className="text-success mt-0.5 flex-shrink-0" />
                          <div>
                            <span className="text-[13px] font-medium">Punto #{u.id}</span>
                            <span className="text-[12px] text-muted ml-2">→ {u.completado ? 'completado' : 'pendiente'}</span>
                            {u.reason && <p className="text-[11px] text-muted mt-0.5">{u.reason}</p>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {result.task_updates.length === 0 && result.plan_updates.length === 0 && (
                  <p className="text-[12px] text-muted">No se detectaron cambios para aplicar.</p>
                )}
              </div>
            )}
          </div>

          {/* Recent commits */}
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <GitCommit size={14} className="text-muted" />
                <h3 className="font-semibold text-[15px]">Commits recientes</h3>
              </div>
              <button onClick={loadCommits} className="btn-ghost text-[12px]">
                <RefreshCw size={12} /> Actualizar
              </button>
            </div>

            {loadingCommits ? (
              <div className="space-y-2">
                {[1,2,3].map(i => <div key={i} className="h-12 rounded-xl animate-pulse bg-neutral-100 dark:bg-slate-800" />)}
              </div>
            ) : commits.length === 0 ? (
              <p className="text-[13px] text-muted text-center py-8">Sin commits disponibles.</p>
            ) : (
              <div className="space-y-1">
                {commits.map((c, i) => (
                  <div key={i} className="flex items-start gap-3 py-2.5 border-b border-border/50 dark:border-slate-700/50 last:border-0">
                    <code className="text-[11px] text-accent bg-accent/10 px-1.5 py-0.5 rounded font-mono flex-shrink-0 mt-0.5">
                      {c.sha}
                    </code>
                    <div className="flex-1 min-w-0">
                      <p className="text-[13px] text-primary dark:text-slate-200 truncate">{c.message}</p>
                      <p className="text-[11px] text-muted">{c.author} · {c.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

function ModalNuevoPunto({ proyectoId, onClose, onSaved, orden }) {
  const [form, setForm] = useState({ titulo: '', descripcion: '' })
  const [saving, setSaving] = useState(false)
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handle = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.post(`/api/proyectos/${proyectoId}/plan`, { ...form, orden })
      onSaved()
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-primary/30 backdrop-blur-sm z-50 grid place-items-center p-6"
      onClick={onClose}>
      <div className="card p-7 max-w-md w-full shadow-lift animate-scale-in" onClick={e => e.stopPropagation()}>
        <h2 className="hero-title text-xl mb-5">Nuevo punto de acción.</h2>
        <form onSubmit={handle} className="space-y-4">
          <div>
            <label className="label">Título del punto</label>
            <input className="input" required placeholder="Entregable o hito..." value={form.titulo} onChange={set('titulo')} />
          </div>
          <div>
            <label className="label">Descripción (opcional)</label>
            <textarea className="textarea" rows={2} placeholder="Detalles..." value={form.descripcion} onChange={set('descripcion')} />
          </div>
          <div className="flex gap-3 pt-1">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-accent flex-1 disabled:opacity-50">
              {saving ? 'Agregando...' : 'Agregar punto'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
