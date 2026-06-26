import { useEffect, useRef, useState } from 'react'
import { Bot, Send, Sparkles, CheckCircle2, AlertTriangle, Clock, Loader2, Check, X } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'

const ESTADO_TAREA = {
  pendiente:        { label: 'Pendiente',   chip: 'chip-muted',    icon: Clock },
  en_proceso:       { label: 'En proceso',  chip: 'chip-warn',     icon: Loader2 },
  completado:       { label: 'Completado',  chip: 'chip-success',  icon: CheckCircle2 },
  error:            { label: 'Error',       chip: 'chip-danger',   icon: AlertTriangle },
  requiere_aprobacion: { label: 'Aprobación', chip: 'chip-accent', icon: AlertTriangle },
}

export default function Agentes() {
  const [chat, setChat] = useState([])
  const [catalogo, setCatalogo] = useState([])
  const [tareas, setTareas] = useState([])
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const chatEndRef = useRef(null)

  const cargar = () => {
    api.get('/api/agentes/chat').then(r => setChat(r.data)).catch(() => {})
    api.get('/api/agentes/tareas').then(r => setTareas(r.data)).catch(() => {})
  }

  useEffect(() => {
    api.get('/api/agentes/catalogo').then(r => setCatalogo(r.data)).catch(() => {})
    cargar()
    const t = setInterval(cargar, 5000)   // refresco en vivo (polling)
    return () => clearInterval(t)
  }, [])

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [chat.length])

  const enviar = async e => {
    e.preventDefault()
    const msg = texto.trim()
    if (!msg) return
    setEnviando(true)
    setTexto('')
    try {
      await api.post('/api/agentes/chat', { contenido: msg, canal: 'agentes' })
      cargar()
    } catch {
      toast.error('No se pudo enviar el mensaje')
      setTexto(msg)
    } finally {
      setEnviando(false)
    }
  }

  const aprobar = async (mid, estado) => {
    try {
      await api.patch(`/api/agentes/chat/${mid}/estado?estado=${estado}`)
      cargar()
    } catch {
      toast.error('No se pudo actualizar')
    }
  }

  return (
    <div className="animate-fade-in">
      <header className="mb-8">
        <div className="hero-eyebrow">Equipo de IA</div>
        <h1 className="hero-title text-4xl md:text-5xl mb-2">Centro de Agentes.</h1>
        <p className="hero-sub">Hablá con el orquestador. Él reparte el trabajo a los subagentes y te reporta.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* ── Chat con el orquestador ── */}
        <div className="lg:col-span-2 card p-0 flex flex-col h-[70vh]">
          <div className="px-5 py-4 border-b border-border flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-accent text-white flex items-center justify-center">
              <Bot size={16} />
            </div>
            <div>
              <div className="font-bold text-[14px] tracking-tight">Orquestador</div>
              <div className="text-[11px] text-muted">Punto de entrada del equipo</div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
            {chat.length === 0 ? (
              <div className="text-center text-muted text-[13px] mt-10">
                <Sparkles size={20} className="mx-auto mb-2 opacity-50" />
                Escribile al orquestador para empezar.<br />
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
            <input className="input flex-1" placeholder="Pedile algo al orquestador..."
              value={texto} onChange={e => setTexto(e.target.value)} />
            <button type="submit" disabled={enviando} className="btn-accent disabled:opacity-50">
              {enviando ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
            </button>
          </form>
        </div>

        {/* ── Panel lateral: equipo + tareas ── */}
        <div className="space-y-6">
          {/* Catálogo de agentes agrupado por área */}
          <div className="card p-5">
            <div className="font-bold text-[13px] tracking-tight mb-3">El equipo</div>
            <div className="space-y-4">
              {['Marketing', 'Comercial', 'Desarrollo'].map(area => {
                const delArea = catalogo.filter(a => a.area === area)
                if (!delArea.length) return null
                return (
                  <div key={area}>
                    <div className="text-[10px] uppercase tracking-wide text-accent font-semibold mb-1.5">{area}</div>
                    <div className="space-y-2">
                      {delArea.map(a => (
                        <div key={a.agente} className="flex items-start gap-2.5">
                          <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${a.listo ? 'bg-success' : 'bg-warn'}`} />
                          <div className="min-w-0">
                            <div className={`text-[13px] ${a.director ? 'font-bold' : 'font-semibold'}`}>
                              {a.nombre}{a.director && ' ★'}
                            </div>
                            <div className="text-[11px] text-muted">{a.rol}</div>
                            {a.requiere && <div className="text-[10px] text-warn mt-0.5">⚠ {a.requiere}</div>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Feed de tareas */}
          <div className="card p-5">
            <div className="font-bold text-[13px] tracking-tight mb-3">Tareas del equipo</div>
            {tareas.length === 0 ? (
              <div className="text-[12px] text-muted">Sin tareas todavía.</div>
            ) : (
              <div className="space-y-2 max-h-[40vh] overflow-y-auto">
                {tareas.map(t => {
                  const cfg = ESTADO_TAREA[t.estado] || ESTADO_TAREA.pendiente
                  return (
                    <div key={t.id} className="border border-border rounded-xl p-3">
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="text-[12px] font-semibold capitalize">{t.agente}</span>
                        <span className={cfg.chip}>{cfg.label}</span>
                      </div>
                      <div className="text-[11px] text-muted line-clamp-2">{t.instruccion}</div>
                      {t.resultado && (
                        <div className="text-[11px] text-success mt-1 line-clamp-2">→ {t.resultado}</div>
                      )}
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
