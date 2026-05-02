import { useEffect, useState } from 'react'
import { Plus, Check, Clock, Filter, CheckSquare } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'
import { SkeletonRow, SkeletonStats } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const STATUS_LABEL = { pendiente:'Pendiente', en_progreso:'En progreso', revision:'Revisión', completada:'Completada', bloqueada:'Bloqueada' }
const STATUS_CHIP  = { pendiente:'chip-muted', en_progreso:'chip-accent', revision:'chip-warn', completada:'chip-success', bloqueada:'chip-danger' }
const PRIO_CHIP    = { baja:'chip-muted', media:'chip-primary', alta:'chip-warn', urgente:'chip-danger' }
const PRIO_LABEL   = { baja:'Baja', media:'Media', alta:'Alta', urgente:'Urgente' }

const FILTROS_STATUS = [
  { label:'Todas', value:'' },
  { label:'Pendientes', value:'pendiente' },
  { label:'En progreso', value:'en_progreso' },
  { label:'Revisión', value:'revision' },
  { label:'Completadas', value:'completada' },
]

export default function Tareas() {
  const [tareas, setTareas] = useState([])
  const [proyectos, setProyectos] = useState([])
  const [filtroStatus, setFiltroStatus] = useState('')
  const [filtroProyecto, setFiltroProyecto] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    Promise.all([
      api.get('/api/tareas'),
      api.get('/api/proyectos'),
    ]).then(([t, p]) => {
      setTareas(t.data)
      setProyectos(p.data)
      setLoading(false)
    })
  }
  useEffect(() => { load() }, [])

  const cambiarStatus = async (id, status) => {
    try {
      await api.patch(`/api/tareas/${id}`, { status })
      toast.success(status === 'completada' ? '✓ Tarea completada' : `Estado: ${STATUS_LABEL[status]}`)
      load()
    } catch {
      toast.error('No se pudo cambiar el estado')
    }
  }

  const filtradas = tareas.filter(t => {
    if (filtroStatus && t.status !== filtroStatus) return false
    if (filtroProyecto && t.proyecto_id !== parseInt(filtroProyecto)) return false
    return true
  })

  const proyectoNombre = id => proyectos.find(p => p.id === id)?.nombre ?? '—'
  const proyectoColor  = id => proyectos.find(p => p.id === id)?.color ?? '#6366F1'

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Gestión</div>
        <h1 className="hero-title text-5xl md:text-6xl mb-3">Tareas.</h1>
        <p className="hero-sub">Todas las tareas, todos los proyectos.</p>
      </header>

      {/* Filtros */}
      <div className="flex flex-wrap gap-3 mb-8">
        <div className="flex gap-2 flex-wrap">
          {FILTROS_STATUS.map(f => {
            const count = f.value ? tareas.filter(t => t.status === f.value).length : tareas.length
            return (
              <button key={f.value} onClick={() => setFiltroStatus(f.value)}
                className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
                  filtroStatus === f.value
                    ? 'bg-primary text-neutral-50 shadow-soft'
                    : 'bg-white text-muted hover:bg-neutral-200/70 border border-border'
                }`}>
                {f.label} <span className="ml-1 opacity-60">({count})</span>
              </button>
            )
          })}
        </div>

        <div className="flex items-center gap-2 ml-auto">
          <Filter size={13} className="text-muted" />
          <select className="input !py-2 !px-3 !rounded-full w-auto text-[13px]"
            value={filtroProyecto} onChange={e => setFiltroProyecto(e.target.value)}>
            <option value="">Todos los proyectos</option>
            {proyectos.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
          </select>
        </div>
      </div>

      {/* Resumen buckets */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label:'Pendientes', status:'pendiente', color:'#64748B' },
          { label:'En progreso', status:'en_progreso', color:'#6366F1' },
          { label:'Completadas', status:'completada', color:'#059669' },
        ].map(b => {
          const count = tareas.filter(t => t.status === b.status).length
          return (
            <div key={b.status} className="card p-5">
              <div className="stat-label">{b.label}</div>
              <div className="hero-title text-4xl mt-1" style={{ color: b.color }}>{count}</div>
            </div>
          )
        })}
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1,2,3,4,5].map(i => <SkeletonRow key={i} />)}
        </div>
      ) : filtradas.length === 0 ? (
        <EmptyState
          icon={CheckSquare}
          title="No hay tareas con estos filtros"
          description={tareas.length === 0
            ? 'Las tareas se crean desde el detalle de cada proyecto, o usando "Generar con IA".'
            : 'Probá quitar algún filtro para ver más resultados.'}
          action={tareas.length > 0 ? () => { setFiltroStatus(''); setFiltroProyecto('') } : null}
          actionLabel="Limpiar filtros"
        />
      ) : (
        <div className="space-y-2">
          {filtradas.map(t => {
            const horas = Math.floor(t.minutos_trabajados / 60)
            const mins  = t.minutos_trabajados % 60
            return (
              <div key={t.id} className="card p-4 flex items-center gap-4 card-hover group">
                <button onClick={() => cambiarStatus(t.id, t.status === 'completada' ? 'pendiente' : 'completada')}
                  className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center flex-shrink-0 transition-all ${
                    t.status === 'completada' ? 'border-success bg-success text-white' : 'border-border hover:border-accent'
                  }`}>
                  {t.status === 'completada' && <Check size={12} />}
                </button>

                <div className="flex-1 min-w-0">
                  <div className={`font-medium text-[14px] tracking-tight ${t.status === 'completada' ? 'line-through text-muted' : ''}`}>
                    {t.titulo}
                  </div>
                  <div className="flex items-center gap-2 mt-1 flex-wrap">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: proyectoColor(t.proyecto_id) }} />
                      <span className="text-[11px] text-muted">{proyectoNombre(t.proyecto_id)}</span>
                    </div>
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
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
