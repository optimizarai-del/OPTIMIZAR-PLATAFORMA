import { useEffect, useState, useRef, useCallback } from 'react'
import {
  Bot, Send, Search, CheckCircle2, XCircle, Clock, AlertTriangle,
  Sparkles, User, Loader2, Target,
} from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'

// Refresco del chat y los jobs (chat "siempre activo")
const POLL_MS = 8000

const JOB_STATUS = {
  pendiente:  { label: 'Pendiente',  cls: 'chip-muted',   icon: Clock },
  procesando: { label: 'Procesando', cls: 'chip-accent',  icon: Loader2 },
  completado: { label: 'Completado', cls: 'chip-success', icon: CheckCircle2 },
  error:      { label: 'Error',      cls: 'chip-danger',  icon: AlertTriangle },
}

export default function Prospeccion() {
  const [msgs, setMsgs] = useState([])
  const [jobs, setJobs] = useState([])
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [loading, setLoading] = useState(true)
  const scrollRef = useRef(null)
  const aliveRef = useRef(true)
  // Mientras hay una acción local en vuelo (enviar mensaje / aprobar) pausamos el
  // merge del poll para que no pise el cambio optimista antes de que el backend persista.
  const busyRef = useRef(false)

  // Mergea por id: conserva los mensajes locales que el servidor todavía no devolvió.
  const mergeMsgs = (prev, server) => {
    const ids = new Set(server.map(m => m.id))
    const localPendientes = prev.filter(m => !ids.has(m.id))
    return [...server, ...localPendientes].sort((a, b) => a.id - b.id)
  }

  const cargar = useCallback((silencioso = false) => {
    Promise.all([
      api.get('/api/crm/chat'),
      api.get('/api/crm/lead-jobs'),
    ]).then(([c, j]) => {
      if (!aliveRef.current) return
      if (!busyRef.current) setMsgs(prev => mergeMsgs(prev, c.data))
      setJobs(j.data)
    }).catch((err) => {
      if (!silencioso && !err?.handled) toast.error('No se pudo cargar el chat del equipo.')
    }).finally(() => { if (aliveRef.current) setLoading(false) })
  }, [])

  useEffect(() => {
    aliveRef.current = true
    cargar()
    const t = setInterval(() => cargar(true), POLL_MS)
    return () => { aliveRef.current = false; clearInterval(t) }
  }, [cargar])

  // auto-scroll al último mensaje
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [msgs])

  const enviar = async (e) => {
    e.preventDefault()
    const contenido = texto.trim()
    if (!contenido) return
    setEnviando(true)
    busyRef.current = true
    try {
      const { data } = await api.post('/api/crm/chat', { contenido })
      setMsgs(m => [...m, data])
      setTexto('')
    } catch (err) {
      if (!err?.handled) toast.error('No se pudo enviar el mensaje.')
    } finally {
      setEnviando(false)
      busyRef.current = false
    }
  }

  const decidir = async (msg, estado) => {
    busyRef.current = true
    try {
      const { data } = await api.patch(`/api/crm/chat/${msg.id}/estado?estado=${estado}`)
      setMsgs(m => m.map(x => x.id === msg.id ? data : x))
      toast.success(estado === 'aprobado' ? 'Acción aprobada' : 'Acción rechazada')
    } catch (err) {
      if (!err?.handled) toast.error('No se pudo registrar la decisión.')
    } finally {
      busyRef.current = false
    }
  }

  return (
    <div className="space-y-7 animate-fade-in">
      {/* ── Header ── */}
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <div className="hero-eyebrow !mb-1.5">Comercial · Equipo IA</div>
          <h1 className="text-3xl md:text-4xl hero-title">Prospección autónoma</h1>
        </div>
        <div className="chip-accent items-center gap-1.5">
          <Sparkles size={13} /> Equipo de Venta y Prospección
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* ── Chat (2 columnas) ── */}
        <div className="lg:col-span-2 card p-0 overflow-hidden flex flex-col h-[640px]">
          <div className="flex items-center gap-2.5 px-5 py-3.5 border-b border-neutral-200/70 dark:border-slate-700/60">
            <div className="w-8 h-8 rounded-xl bg-accent/10 flex items-center justify-center">
              <Bot size={16} className="text-accent" />
            </div>
            <div>
              <div className="text-[13.5px] font-semibold tracking-tight text-primary dark:text-slate-100">
                Orquestador del equipo
              </div>
              <div className="text-[11px] text-muted">Reporta, pide aprobaciones y escala riesgos</div>
            </div>
          </div>

          {/* mensajes */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
            {loading ? (
              <div className="flex items-center justify-center h-full text-muted">
                <Loader2 className="animate-spin" size={18} />
              </div>
            ) : msgs.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center text-muted gap-2">
                <Bot size={28} className="text-muted/40" />
                <p className="text-[13px] max-w-xs">
                  Todavía no hay conversación. El orquestador escribirá acá cuando corra un ciclo,
                  o podés escribirle vos abajo.
                </p>
              </div>
            ) : (
              msgs.map(m => <Mensaje key={m.id} m={m} onDecidir={decidir} />)
            )}
          </div>

          {/* input */}
          <form onSubmit={enviar} className="flex items-center gap-2 px-4 py-3 border-t border-neutral-200/70 dark:border-slate-700/60">
            <input
              className="input !rounded-full flex-1"
              placeholder="Escribile al equipo…"
              value={texto}
              onChange={e => setTexto(e.target.value)}
            />
            <button type="submit" disabled={enviando || !texto.trim()} className="btn-accent !rounded-full !px-3.5">
              {enviando ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
            </button>
          </form>
        </div>

        {/* ── Buscar leads + jobs ── */}
        <div className="space-y-5">
          <BuscarLeads onCreado={() => cargar(true)} />
          <ListaJobs jobs={jobs} loading={loading} />
        </div>
      </div>
    </div>
  )
}

// ── Burbuja de mensaje ────────────────────────────────────────────────────────
function Mensaje({ m, onDecidir }) {
  const esHumano = m.rol === 'humano'
  const esperando = m.requiere_aprobacion && m.estado === 'esperando'
  return (
    <div className={`flex gap-2.5 ${esHumano ? 'flex-row-reverse' : ''}`}>
      <div className={`w-7 h-7 rounded-lg shrink-0 flex items-center justify-center
        ${esHumano ? 'bg-primary/10 dark:bg-slate-700' : 'bg-accent/10'}`}>
        {esHumano ? <User size={14} className="text-primary dark:text-slate-200" /> : <Bot size={14} className="text-accent" />}
      </div>
      <div className={`max-w-[80%] ${esHumano ? 'items-end' : 'items-start'} flex flex-col`}>
        <div className={`rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed whitespace-pre-wrap
          ${esHumano
            ? 'bg-primary text-neutral-50 dark:bg-accent rounded-tr-sm'
            : 'bg-neutral-100 dark:bg-slate-800 text-primary dark:text-slate-100 rounded-tl-sm'}`}>
          {m.contenido}
        </div>

        {/* gate de aprobación */}
        {esperando && (
          <div className="flex items-center gap-2 mt-2">
            <button onClick={() => onDecidir(m, 'aprobado')} className="btn-success !py-1 !px-2.5 !text-[12px]">
              <CheckCircle2 size={13} /> Aprobar
            </button>
            <button onClick={() => onDecidir(m, 'rechazado')} className="btn-ghost !py-1 !px-2.5 !text-[12px]">
              <XCircle size={13} /> Rechazar
            </button>
          </div>
        )}
        {m.requiere_aprobacion && m.estado === 'aprobado' && (
          <span className="chip-success mt-1.5 !text-[11px]"><CheckCircle2 size={11} /> Aprobado</span>
        )}
        {m.requiere_aprobacion && m.estado === 'rechazado' && (
          <span className="chip-danger mt-1.5 !text-[11px]"><XCircle size={11} /> Rechazado</span>
        )}
      </div>
    </div>
  )
}

// ── Form de búsqueda de leads (encola un lead-job) ────────────────────────────
const ICP_EMPTY = { rubro: '', tamano: '', cargo: '', geografia: 'Argentina', idioma: 'es' }

function BuscarLeads({ onCreado }) {
  const [icp, setIcp] = useState(ICP_EMPTY)
  const [cantidad, setCantidad] = useState(15)
  const [fundamento, setFundamento] = useState('')
  const [enviando, setEnviando] = useState(false)
  const set = (k) => (e) => setIcp(v => ({ ...v, [k]: e.target.value }))

  const submit = async (e) => {
    e.preventDefault()
    if (!icp.rubro.trim()) { toast.error('Indicá al menos el rubro.'); return }
    const n = parseInt(cantidad, 10)
    if (!Number.isFinite(n) || n < 1 || n > 50) {
      toast.error('La cantidad debe ser un número entre 1 y 50.'); return
    }
    setEnviando(true)
    try {
      await api.post('/api/crm/lead-jobs', {
        icp, cantidad: n, fundamento: fundamento || null,
      })
      toast.success('Búsqueda encolada. El equipo la tomará en la próxima corrida.')
      setFundamento(''); onCreado()
    } catch (err) {
      if (!err?.handled) toast.error('No se pudo encolar la búsqueda.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 mb-4">
        <Search size={16} className="text-accent" />
        <h3 className="text-[14px] font-semibold tracking-tight text-primary dark:text-slate-100">Buscar leads</h3>
      </div>
      <form onSubmit={submit} className="space-y-3">
        <div>
          <label className="label">Rubro / tipo de cliente *</label>
          <input className="input" placeholder="Gimnasios, clínicas, estudios contables, agencias…" value={icp.rubro} onChange={set('rubro')} />
          <p className="text-[11px] text-muted mt-1">El equipo busca cualquier rubro que indiques acá.</p>
        </div>
        <div className="grid grid-cols-2 gap-2.5">
          <div>
            <label className="label">Tamaño</label>
            <input className="input" placeholder="5–50 empleados" value={icp.tamano} onChange={set('tamano')} />
          </div>
          <div>
            <label className="label">Cargo</label>
            <input className="input" placeholder="Socio / dueño" value={icp.cargo} onChange={set('cargo')} />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2.5">
          <div>
            <label className="label">Geografía</label>
            <input className="input" value={icp.geografia} onChange={set('geografia')} />
          </div>
          <div>
            <label className="label">Idioma</label>
            <input className="input" value={icp.idioma} onChange={set('idioma')} />
          </div>
        </div>
        <div>
          <label className="label">Cantidad</label>
          <input className="input" type="number" min="1" max="50" value={cantidad} onChange={e => setCantidad(e.target.value)} />
        </div>
        <div>
          <label className="label">Fundamento (opcional)</label>
          <textarea className="textarea" rows={2} placeholder="Por qué este segmento hoy…"
                    value={fundamento} onChange={e => setFundamento(e.target.value)} />
        </div>
        <button type="submit" disabled={enviando} className="btn-accent w-full">
          {enviando ? <Loader2 size={15} className="animate-spin" /> : <Target size={15} />}
          {enviando ? 'Encolando…' : 'Encolar búsqueda'}
        </button>
      </form>
    </div>
  )
}

// ── Lista de jobs encolados ───────────────────────────────────────────────────
function ListaJobs({ jobs, loading }) {
  return (
    <div className="card p-5">
      <h3 className="text-[14px] font-semibold tracking-tight text-primary dark:text-slate-100 mb-3">
        Búsquedas recientes
      </h3>
      {loading ? (
        <div className="text-muted text-[13px] py-2">Cargando…</div>
      ) : jobs.length === 0 ? (
        <div className="text-muted text-[12.5px] py-2">Todavía no encolaste búsquedas.</div>
      ) : (
        <div className="space-y-2 max-h-[280px] overflow-y-auto">
          {jobs.map(j => {
            const st = JOB_STATUS[j.status] || JOB_STATUS.pendiente
            const Icon = st.icon
            return (
              <div key={j.id} className="rounded-2xl border border-neutral-200/70 dark:border-slate-700/60 p-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[12.5px] font-medium text-primary dark:text-slate-100 truncate">
                    {j.icp?.rubro || 'Sin rubro'} · {j.cantidad}
                  </span>
                  <span className={`${st.cls} !text-[10.5px] shrink-0`}>
                    <Icon size={10} className={j.status === 'procesando' ? 'animate-spin' : ''} /> {st.label}
                  </span>
                </div>
                {j.icp?.geografia && (
                  <div className="text-[11px] text-muted mt-1 truncate">{j.icp.geografia}</div>
                )}
                {j.resumen && (
                  <div className="text-[11px] text-muted mt-1.5 line-clamp-2">{j.resumen}</div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
