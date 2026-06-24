import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, FileText, Calendar, User, Sparkles, CheckCircle2, AlertTriangle, RefreshCw, Loader2 } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'
import { SkeletonRow } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const STATUS_LABEL = { nuevo:'Nuevo', evaluacion:'En evaluación', aprobado:'Aprobado', rechazado:'Rechazado', convertido:'Convertido' }
const STATUS_CHIP  = { nuevo:'chip-accent', evaluacion:'chip-warn', aprobado:'chip-success', rechazado:'chip-danger', convertido:'chip-primary' }

const FILTROS = [
  { label:'Todos', value:'' },
  { label:'Nuevos', value:'nuevo' },
  { label:'En evaluación', value:'evaluacion' },
  { label:'Aprobados', value:'aprobado' },
  { label:'Convertidos', value:'convertido' },
]

export default function Requerimientos() {
  const nav = useNavigate()
  const [reqs, setReqs] = useState([])
  const [filtro, setFiltro] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    api.get('/api/requerimientos')
      .then(r => setReqs(r.data))
      .catch(() => toast.error('No se pudieron cargar los requerimientos.'))
      .finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const [analizando, setAnalizando] = useState(null)

  const cambiarStatus = async (id, status) => {
    try {
      await api.patch(`/api/requerimientos/${id}`, { status })
      toast.success(`Estado: ${STATUS_LABEL[status]}`)
      load()
    } catch {
      toast.error('No se pudo cambiar el estado')
    }
  }

  const reanalizar = async (id) => {
    setAnalizando(id)
    try {
      await api.post(`/api/requerimientos/${id}/analizar`)
      toast.success('Análisis actualizado')
      load()
    } catch {
      toast.error('No se pudo re-analizar')
    } finally {
      setAnalizando(null)
    }
  }

  const filtrados = filtro ? reqs.filter(r => r.status === filtro) : reqs

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Comercial</div>
        <div className="flex items-end justify-between flex-wrap gap-4">
          <div>
            <h1 className="hero-title text-5xl md:text-6xl mb-3">Requerimientos.</h1>
            <p className="hero-sub">Handovers de ventas a desarrollo.</p>
          </div>
          <button onClick={() => nav('/requerimientos/nuevo')} className="btn-accent">
            <Plus size={14} /> Cargar requerimiento
          </button>
        </div>
      </header>

      {/* Filtros */}
      <div className="flex gap-2 mb-8 flex-wrap">
        {FILTROS.map(f => {
          const count = f.value ? reqs.filter(r => r.status === f.value).length : reqs.length
          return (
            <button key={f.value} onClick={() => setFiltro(f.value)}
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
        <div className="space-y-3">
          {[1,2,3].map(i => <SkeletonRow key={i} />)}
        </div>
      ) : filtrados.length === 0 ? (
        <EmptyState
          icon={FileText}
          title={filtro ? `Sin requerimientos en estado "${STATUS_LABEL[filtro]}"` : 'No hay requerimientos todavía'}
          description={filtro
            ? 'Probá con otro filtro o cargá un requerimiento nuevo.'
            : 'Cargá tu primer requerimiento desde Comercial → Cargar Requerimiento.'}
          action={() => nav('/requerimientos/nuevo')}
          actionLabel="+ Cargar primer requerimiento"
        />
      ) : (
        <div className="space-y-3">
          {filtrados.map(r => (
            <div key={r.id} className="card p-5 card-hover">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={STATUS_CHIP[r.status]}>{STATUS_LABEL[r.status]}</span>
                    {r.sector && <span className="chip-muted">{r.sector}</span>}
                  </div>
                  <div className="font-bold text-[16px] tracking-tight">{r.nombre_cliente}</div>
                  {r.nombre_proceso && (
                    <div className="text-[13px] text-muted mt-1">Proceso: {r.nombre_proceso}</div>
                  )}
                  <div className="flex items-center gap-4 mt-3 text-[12px] text-muted flex-wrap">
                    {r.responsable_comercial && (
                      <span className="flex items-center gap-1"><User size={11} /> {r.responsable_comercial}</span>
                    )}
                    {r.fecha_entrega && (
                      <span className="flex items-center gap-1">
                        <Calendar size={11} /> {new Date(r.fecha_entrega).toLocaleDateString('es-AR')}
                      </span>
                    )}
                    {r.volumen_proceso && <span>Vol: {r.volumen_proceso}</span>}
                    {r.tiempo_por_proceso && <span>Tiempo: {r.tiempo_por_proceso}</span>}
                  </div>
                </div>
                <div className="flex gap-2 flex-wrap">
                  {r.status === 'nuevo' && (
                    <button onClick={() => cambiarStatus(r.id, 'evaluacion')} className="btn-secondary">
                      Iniciar evaluación
                    </button>
                  )}
                  {r.status === 'evaluacion' && (
                    <>
                      <button onClick={() => cambiarStatus(r.id, 'aprobado')} className="btn-success">Aprobar</button>
                      <button onClick={() => cambiarStatus(r.id, 'rechazado')} className="btn-danger">Rechazar</button>
                    </>
                  )}
                  {r.status === 'aprobado' && (
                    <button onClick={() => cambiarStatus(r.id, 'convertido')} className="btn-accent">
                      → Convertir en proyecto
                    </button>
                  )}
                </div>
              </div>

              {/* Análisis IA: ¿lo cubre algún servicio existente? */}
              <AnalisisIA r={r} analizando={analizando === r.id} onReanalizar={() => reanalizar(r.id)} />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function AnalisisIA({ r, analizando, onReanalizar }) {
  const estado = r.analisis_estado || 'pendiente'

  const base = "mt-4 pt-4 border-t border-border flex items-start justify-between gap-3 flex-wrap"
  const reBtn = (
    <button onClick={onReanalizar} disabled={analizando}
      className="btn-ghost text-muted text-[12px] shrink-0" title="Volver a analizar">
      {analizando
        ? <Loader2 size={13} className="animate-spin" />
        : <RefreshCw size={13} />}
      {analizando ? 'Analizando...' : 'Re-analizar'}
    </button>
  )

  if (estado === 'cubierto') {
    return (
      <div className={base}>
        <div className="flex items-start gap-2.5 flex-1 min-w-0">
          <CheckCircle2 size={17} className="text-success shrink-0 mt-0.5" />
          <div className="min-w-0">
            <div className="text-[13px] font-semibold text-success flex items-center gap-1.5 flex-wrap">
              <Sparkles size={12} /> Cubierto por: {r.servicio_match_nombre || 'un servicio existente'}
              {typeof r.analisis_confianza === 'number' && (
                <span className="chip-success">{r.analisis_confianza}% confianza</span>
              )}
            </div>
            {r.analisis_justificacion && (
              <div className="text-[12px] text-muted mt-1">{r.analisis_justificacion}</div>
            )}
          </div>
        </div>
        {reBtn}
      </div>
    )
  }

  if (estado === 'no_cubierto' || estado === 'error') {
    return (
      <div className={base}>
        <div className="flex items-start gap-2.5 flex-1 min-w-0">
          <AlertTriangle size={17} className="text-warn shrink-0 mt-0.5" />
          <div className="min-w-0">
            <div className="text-[13px] font-bold text-warn">Consultar con área de desarrollo</div>
            <div className="text-[12px] text-muted mt-1">
              {estado === 'error'
                ? (r.analisis_justificacion || 'No se pudo completar el análisis automático.')
                : (r.analisis_justificacion || 'Ningún servicio del catálogo cubre este requerimiento.')}
            </div>
          </div>
        </div>
        {reBtn}
      </div>
    )
  }

  // pendiente
  return (
    <div className={base}>
      <div className="flex items-center gap-2.5 text-muted">
        <Sparkles size={15} className="shrink-0" />
        <span className="text-[12px]">Análisis de cobertura pendiente.</span>
      </div>
      {reBtn}
    </div>
  )
}
