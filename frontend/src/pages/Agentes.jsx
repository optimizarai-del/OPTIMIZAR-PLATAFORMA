import { useEffect, useMemo, useRef, useState } from 'react'
import { Bot, Send, Sparkles, CheckCircle2, AlertTriangle, Clock, Loader2, Check, X, Activity } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'

// chip = badge de estado · dot = color del puntito del agente · border = borde de la tarjeta
// pulse = el agente "se prende" (anima) cuando está trabajando
const ESTADO_TAREA = {
  pendiente:        { label: 'Pendiente',   chip: 'chip-muted',    icon: Clock,         dot: 'bg-neutral-300 dark:bg-slate-600', border: 'border-border' },
  en_proceso:       { label: 'Trabajando',  chip: 'chip-warn',     icon: Loader2,       dot: 'bg-warn',    border: 'border-warn/50', pulse: true },
  completado:       { label: 'Completado',  chip: 'chip-success',  icon: CheckCircle2,  dot: 'bg-success', border: 'border-success/40' },
  error:            { label: 'Error',       chip: 'chip-danger',   icon: AlertTriangle, dot: 'bg-danger',  border: 'border-danger/40' },
  requiere_aprobacion: { label: 'Aprobación', chip: 'chip-accent', icon: AlertTriangle, dot: 'bg-accent',  border: 'border-accent/50', pulse: true },
}

// "hace 3 min" — tiempo relativo corto
function hace(ts) {
  if (!ts) return ''
  const s = Math.max(0, (Date.now() - new Date(ts).getTime()) / 1000)
  if (s < 60) return 'recién'
  if (s < 3600) return `hace ${Math.floor(s / 60)} min`
  if (s < 86400) return `hace ${Math.floor(s / 3600)} h`
  return `hace ${Math.floor(s / 86400)} d`
}

const DIRECTORES = [
  { canal: 'marketing',  nombre: 'Director de Marketing', area: 'Marketing' },
  { canal: 'comercial',  nombre: 'Director Comercial',    area: 'Comercial' },
  { canal: 'desarrollo', nombre: 'Director de Desarrollo', area: 'Desarrollo' },
]

export default function Agentes() {
  const [canal, setCanal] = useState('comercial')
  const [chat, setChat] = useState([])
  const [catalogo, setCatalogo] = useState([])
  const [tareas, setTareas] = useState([])
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const chatEndRef = useRef(null)
  const busyRef = useRef(false)   // bloquea el polling mientras hay una acción del usuario en curso

  const director = DIRECTORES.find(d => d.canal === canal)

  // Agentes que pertenecen al área del director actual (para filtrar tareas/equipo)
  const agentesDelArea = useMemo(
    () => new Set(catalogo.filter(a => a.area === director?.area && !a.director).map(a => a.agente)),
    [catalogo, director?.area]
  )
  // Tareas de este equipo (las tareas vienen ordenadas por created_at desc del backend)
  const tareasArea = useMemo(
    () => tareas.filter(t => agentesDelArea.has(t.agente)),
    [tareas, agentesDelArea]
  )
  // Estado actual de cada agente = su tarea más reciente (la 1ra que aparece, por el orden desc)
  const estadoPorAgente = useMemo(() => {
    const m = {}
    for (const t of tareasArea) if (!m[t.agente]) m[t.agente] = t
    return m
  }, [tareasArea])
  // Quién está trabajando AHORA (tarea en_proceso)
  const trabajandoAhora = useMemo(
    () => Object.values(estadoPorAgente).filter(t => t.estado === 'en_proceso'),
    [estadoPorAgente]
  )

  const cargar = (c = canal) => {
    api.get(`/api/agentes/chat?canal=${c}`).then(r => setChat(r.data)).catch(() => {})
    api.get('/api/agentes/tareas').then(r => setTareas(r.data)).catch(() => {})
  }

  useEffect(() => {
    api.get('/api/agentes/catalogo').then(r => setCatalogo(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    cargar(canal)
    // refresco en vivo (polling): no pisa una acción en vuelo (enviar/aprobar)
    const t = setInterval(() => { if (!busyRef.current) cargar(canal) }, 3000)
    return () => clearInterval(t)
  }, [canal])

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [chat.length])

  const enviar = async e => {
    e.preventDefault()
    const msg = texto.trim()
    if (!msg) return
    setEnviando(true)
    setTexto('')
    busyRef.current = true
    try {
      await api.post('/api/agentes/chat', { contenido: msg, canal })
      cargar(canal)
    } catch {
      toast.error('No se pudo enviar el mensaje')
      setTexto(msg)
    } finally {
      setEnviando(false)
      busyRef.current = false
    }
  }

  const aprobar = async (mid, estado) => {
    busyRef.current = true
    try {
      await api.patch(`/api/agentes/chat/${mid}/estado?estado=${estado}`)
      cargar(canal)
    } catch {
      toast.error('No se pudo actualizar')
    } finally {
      busyRef.current = false
    }
  }

  return (
    <div className="animate-fade-in">
      <header className="mb-6">
        <div className="hero-eyebrow">Equipo de IA</div>
        <h1 className="hero-title text-4xl md:text-5xl mb-2">Centro de Agentes.</h1>
        <p className="hero-sub">Cada Director trabaja independiente, con su propia clave. Elegí con quién hablar.</p>
      </header>

      {/* Pestañas: un chat por Director */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {DIRECTORES.map(d => (
          <button key={d.canal} onClick={() => setCanal(d.canal)}
            className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
              canal === d.canal ? 'bg-primary text-neutral-50 shadow-soft'
                : 'bg-white text-muted hover:bg-neutral-200/70 border border-border'
            }`}>
            {d.nombre}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* ── Chat con el orquestador ── */}
        <div className="lg:col-span-2 card p-0 flex flex-col h-[70vh]">
          <div className="px-5 py-4 border-b border-border flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-accent text-white flex items-center justify-center">
              <Bot size={16} />
            </div>
            <div>
              <div className="font-bold text-[14px] tracking-tight">{director?.nombre || 'Director'}</div>
              <div className="text-[11px] text-muted">Coordina el equipo de {director?.area}</div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
            {chat.length === 0 ? (
              <div className="text-center text-muted text-[13px] mt-10">
                <Sparkles size={20} className="mx-auto mb-2 opacity-50" />
                Escribile al Director para empezar.<br />
                Ej: "Generá 3 piezas de contenido sobre el caso de Gabi".
              </div>
            ) : chat.map(m => (
              <div key={m.id} className={`flex ${m.rol === 'humano' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-[13px] leading-relaxed ${
                  m.rol === 'humano'
                    ? 'bg-primary text-neutral-50'
                    : m.rol === 'sistema'
                      ? 'bg-neutral-200/60 text-muted italic'
                      : 'bg-accent/8 border border-accent/15 text-primary dark:text-slate-100'
                }`}>
                  {m.rol !== 'humano' && (
                    <div className="text-[10px] uppercase tracking-wide opacity-60 mb-1 flex items-center gap-1">
                      <Bot size={10} /> {m.rol}
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{m.contenido}</div>
                  {m.requiere_aprobacion && m.estado === 'esperando' && (
                    <div className="flex gap-2 mt-2">
                      <button onClick={() => aprobar(m.id, 'aprobado')} className="btn-success !py-1 !px-2 text-[11px]">
                        <Check size={11} /> Aprobar
                      </button>
                      <button onClick={() => aprobar(m.id, 'rechazado')} className="btn-danger !py-1 !px-2 text-[11px]">
                        <X size={11} /> Rechazar
                      </button>
                    </div>
                  )}
                  {m.requiere_aprobacion && m.estado !== 'esperando' && (
                    <div className={`text-[10px] mt-1 font-semibold ${m.estado === 'aprobado' ? 'text-success' : 'text-danger'}`}>
                      {m.estado === 'aprobado' ? '✓ Aprobado' : '✗ Rechazado'}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={enviar} className="p-3 border-t border-border flex gap-2">
            <input className="input flex-1" placeholder="Pedile algo al Director..."
              value={texto} onChange={e => setTexto(e.target.value)} />
            <button type="submit" disabled={enviando} className="btn-accent disabled:opacity-50">
              {enviando ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
            </button>
          </form>
        </div>

        {/* ── Panel lateral: equipo + tareas ── */}
        <div className="space-y-6">
          {/* Banner "trabajando ahora" */}
          {trabajandoAhora.length > 0 && (
            <div className="card p-4 border-warn/40 bg-warn/5">
              <div className="flex items-center gap-2 text-[11px] uppercase tracking-wide text-warn font-semibold mb-1.5">
                <Activity size={12} className="animate-pulse" /> Trabajando ahora
              </div>
              {trabajandoAhora.map(t => (
                <div key={t.id} className="text-[12px]">
                  <span className="font-bold capitalize">{t.agente}</span>
                  <span className="text-muted"> — {t.instruccion}</span>
                </div>
              ))}
            </div>
          )}

          {/* Catálogo de agentes — se prenden según su estado en vivo */}
          <div className="card p-5">
            <div className="font-bold text-[13px] tracking-tight mb-3">Equipo de {director?.area}</div>
            <div className="space-y-4">
              {[director?.area].filter(Boolean).map(area => {
                const delArea = catalogo.filter(a => a.area === area)
                if (!delArea.length) return null
                return (
                  <div key={area}>
                    <div className="text-[10px] uppercase tracking-wide text-accent font-semibold mb-1.5">{area}</div>
                    <div className="space-y-2">
                      {delArea.map(a => {
                        const t = estadoPorAgente[a.agente]
                        const cfg = t ? (ESTADO_TAREA[t.estado] || ESTADO_TAREA.pendiente) : null
                        const activo = cfg?.pulse
                        return (
                          <div key={a.agente}
                            className={`flex items-start gap-2.5 rounded-lg px-1.5 py-1 -mx-1.5 transition-colors ${
                              activo ? 'bg-warn/10' : ''}`}>
                            <div className="relative mt-1.5 shrink-0">
                              {/* puntito: estado en vivo si hay tarea, si no el de "listo/falta credencial" */}
                              <div className={`w-2 h-2 rounded-full ${cfg ? cfg.dot : (a.listo ? 'bg-success' : 'bg-warn')}`} />
                              {activo && <div className={`absolute inset-0 w-2 h-2 rounded-full ${cfg.dot} animate-ping`} />}
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-1.5">
                                <span className={`text-[13px] ${a.director ? 'font-bold' : 'font-semibold'}`}>
                                  {a.nombre}{a.director && ' ★'}
                                </span>
                                {cfg && <span className={`text-[9px] uppercase tracking-wide font-semibold ${
                                  activo ? 'text-warn' : t.estado === 'completado' ? 'text-success' : 'text-muted'
                                }`}>{cfg.label}</span>}
                              </div>
                              <div className="text-[11px] text-muted">{a.rol}</div>
                              {a.requiere && !cfg && <div className="text-[10px] text-warn mt-0.5">⚠ {a.requiere}</div>}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Feed de tareas — en vivo */}
          <div className="card p-5">
            <div className="font-bold text-[13px] tracking-tight mb-3">Tareas del equipo</div>
            {tareasArea.length === 0 ? (
              <div className="text-[12px] text-muted">Sin tareas todavía.</div>
            ) : (
              <div className="space-y-2 max-h-[40vh] overflow-y-auto">
                {tareasArea.map(t => {
                  const cfg = ESTADO_TAREA[t.estado] || ESTADO_TAREA.pendiente
                  const Icon = cfg.icon
                  return (
                    <div key={t.id} className={`border rounded-xl p-3 transition-colors ${cfg.border} ${
                      cfg.pulse ? 'bg-warn/5' : ''}`}>
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="text-[12px] font-semibold capitalize flex items-center gap-1.5">
                          <Icon size={12} className={
                            t.estado === 'en_proceso' ? 'animate-spin text-warn'
                            : t.estado === 'completado' ? 'text-success'
                            : t.estado === 'requiere_aprobacion' ? 'text-accent' : 'text-muted'} />
                          {t.agente}
                        </span>
                        <span className={cfg.chip}>{cfg.label}</span>
                      </div>
                      <div className="text-[11px] text-muted line-clamp-2">{t.instruccion}</div>
                      {t.resultado && (
                        <div className="text-[11px] text-success mt-1 line-clamp-2">→ {t.resultado}</div>
                      )}
                      <div className="text-[10px] text-muted/60 mt-1">{hace(t.processed_at || t.created_at)}</div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
