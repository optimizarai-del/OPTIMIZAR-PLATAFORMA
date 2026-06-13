import { useEffect, useState, useMemo, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Plus, Building2, TrendingUp, Trophy, Target, X,
  Phone, Mail, Rocket, DollarSign, Zap, GripVertical, Trash2,
} from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'
import { SkeletonCard } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

// ── Definición de etapas del pipeline ──────────────────────────────────────────
const ETAPAS = [
  { key: 'lead',        label: 'Lead',        accent: '#94A3B8', bar: 'bg-neutral-400' },
  { key: 'contactado',  label: 'Contactado',  accent: '#6366F1', bar: 'bg-accent' },
  { key: 'propuesta',   label: 'Propuesta',   accent: '#818CF8', bar: 'bg-accent-400' },
  { key: 'negociacion', label: 'Negociación', accent: '#B45309', bar: 'bg-warn' },
  { key: 'ganado',      label: 'Ganado',      accent: '#059669', bar: 'bg-success' },
  { key: 'perdido',     label: 'Perdido',     accent: '#DC2626', bar: 'bg-danger' },
]

const fmtMoney = (n) =>
  new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
    .format(n || 0)

export default function CRM() {
  const nav = useNavigate()
  const [ops, setOps] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [dragId, setDragId] = useState(null)
  const [overEtapa, setOverEtapa] = useState(null)
  const [modal, setModal] = useState(null)   // null | {} (nueva) | oportunidad (editar)

  const aliveRef = useRef(true)

  const load = useCallback(() => {
    Promise.all([
      api.get('/api/crm/oportunidades'),
      api.get('/api/crm/stats'),
    ]).then(([o, s]) => {
      if (!aliveRef.current) return
      setOps(o.data); setStats(s.data)
    }).catch((err) => {
      if (!err?.handled) toast.error('No se pudo cargar el CRM.')
    }).finally(() => { if (aliveRef.current) setLoading(false) })
  }, [])

  useEffect(() => {
    aliveRef.current = true
    load()
    return () => { aliveRef.current = false }
  }, [load])

  const porEtapa = useMemo(() => {
    const m = Object.fromEntries(ETAPAS.map(e => [e.key, []]))
    for (const op of ops) (m[op.etapa] ||= []).push(op)
    return m
  }, [ops])

  // ── Drag & drop (HTML5 nativo, sin dependencias) ──
  const onDrop = async (etapa) => {
    setOverEtapa(null)
    const op = ops.find(o => o.id === dragId)
    setDragId(null)
    if (!op || op.etapa === etapa) return
    const prev = op.etapa
    // optimista
    setOps(list => list.map(o => o.id === op.id ? { ...o, etapa } : o))
    try {
      await api.patch(`/api/crm/oportunidades/${op.id}`, { etapa })
      const lbl = ETAPAS.find(e => e.key === etapa)?.label
      toast.success(`${op.empresa} → ${lbl}`)
      api.get('/api/crm/stats')
        .then(s => { if (aliveRef.current) setStats(s.data) })
        .catch((err) => { if (!err?.handled) toast.error('No se pudieron actualizar las métricas del CRM.') })
    } catch {
      setOps(list => list.map(o => o.id === op.id ? { ...o, etapa: prev } : o))
      toast.error('No se pudo mover')
    }
  }

  const convertir = async (op) => {
    try {
      const { data } = await api.post(`/api/crm/oportunidades/${op.id}/convertir`)
      toast.success(`Proyecto creado: ${data.nombre}`)
      nav(`/proyecto/${data.id}`)
    } catch (e) {
      toast.error(e.response?.data?.detail || 'No se pudo convertir')
    }
  }

  return (
    <div className="space-y-7 animate-fade-in">
      {/* ── Header ── */}
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <div className="hero-eyebrow !mb-1.5">Comercial · CRM</div>
          <h1 className="text-3xl md:text-4xl hero-title">Pipeline de ventas</h1>
        </div>
        <button onClick={() => setModal({})} className="btn-accent btn-lg">
          <Plus size={18} /> Nueva oportunidad
        </button>
      </div>

      {/* ── Stats ── */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <StatCard icon={TrendingUp} label="Valor en pipeline" value={fmtMoney(stats.valor_pipeline)} accent="text-accent" />
          <StatCard icon={Trophy} label="Ganado" value={fmtMoney(stats.valor_ganado)} accent="text-success" />
          <StatCard icon={Target} label="Oportunidades" value={stats.total_oportunidades} accent="text-primary dark:text-slate-100" />
          <StatCard icon={Zap} label="Win rate" accent="text-warn"
            value={`${stats.ganadas + stats.perdidas > 0
              ? Math.round((stats.ganadas / (stats.ganadas + stats.perdidas)) * 100) : 0}%`} />
        </div>
      )}

      {/* ── Board ── */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : ops.length === 0 ? (
        <EmptyState
          icon={Building2}
          title="Todavía no hay oportunidades"
          description="Cargá tu primera oportunidad de venta o conectá un sistema externo vía la API."
          action={() => setModal({})}
          actionLabel="Nueva oportunidad"
        />
      ) : (
        <div className="flex gap-3 overflow-x-auto pb-4 -mx-1 px-1 snap-x">
          {ETAPAS.map(et => {
            const items = porEtapa[et.key] || []
            const total = items.reduce((s, o) => s + (o.valor_estimado || 0), 0)
            const isOver = overEtapa === et.key
            return (
              <div
                key={et.key}
                onDragOver={(e) => { e.preventDefault(); setOverEtapa(et.key) }}
                onDragLeave={() => setOverEtapa(o => o === et.key ? null : o)}
                onDrop={() => onDrop(et.key)}
                className={`snap-start shrink-0 w-[270px] rounded-3xl p-2.5 transition-colors duration-200
                  ${isOver ? 'bg-accent/5 dark:bg-accent/10 ring-2 ring-accent/30' : 'bg-neutral-100/60 dark:bg-slate-800/40'}`}
              >
                {/* col header */}
                <div className="flex items-center justify-between px-2 py-1.5 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full" style={{ background: et.accent }} />
                    <span className="text-[13px] font-semibold tracking-tight text-primary dark:text-slate-100">{et.label}</span>
                    <span className="chip-muted !px-1.5 !py-0">{items.length}</span>
                  </div>
                  {total > 0 && (
                    <span className="text-[11px] font-medium text-muted tabular-nums">{fmtMoney(total)}</span>
                  )}
                </div>

                <div className="space-y-2 min-h-[60px]">
                  {items.map(op => (
                    <OppCard
                      key={op.id}
                      op={op}
                      etapa={et}
                      dragging={dragId === op.id}
                      onDragStart={() => setDragId(op.id)}
                      onDragEnd={() => { setDragId(null); setOverEtapa(null) }}
                      onClick={() => setModal(op)}
                      onConvertir={() => convertir(op)}
                    />
                  ))}
                  {items.length === 0 && (
                    <div className="text-center text-[11px] text-muted/50 py-6 select-none">
                      Soltá una tarjeta acá
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {modal !== null && (
        <OppModal
          op={modal.id ? modal : null}
          onClose={() => setModal(null)}
          onSaved={() => { setModal(null); load() }}
        />
      )}
    </div>
  )
}

// ── Stat card ───────────────────────────────────────────────────────────────
function StatCard({ icon: Icon, label, value, accent }) {
  return (
    <div className="card card-hover p-4 flex items-center gap-3.5">
      <div className="w-10 h-10 rounded-2xl bg-neutral-100 dark:bg-slate-700/60 flex items-center justify-center shrink-0">
        <Icon size={18} className={accent} strokeWidth={1.8} />
      </div>
      <div className="min-w-0">
        <div className="stat-label truncate">{label}</div>
        <div className={`stat-value text-xl ${accent}`}>{value}</div>
      </div>
    </div>
  )
}

// ── Opportunity card ──────────────────────────────────────────────────────────
function OppCard({ op, etapa, dragging, onDragStart, onDragEnd, onClick, onConvertir }) {
  const ganado = op.etapa === 'ganado'
  return (
    <div
      draggable
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
      onClick={onClick}
      className={`group card card-hover p-3 cursor-pointer select-none border-l-[3px]
        ${dragging ? 'opacity-40 scale-[0.98]' : 'animate-scale-in'}`}
      style={{ borderLeftColor: etapa.accent }}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 text-[11px] font-medium text-muted truncate">
            <Building2 size={11} /> {op.empresa}
          </div>
          <h4 className="text-[13.5px] font-semibold tracking-tight text-primary dark:text-slate-100 leading-snug mt-0.5 line-clamp-2">
            {op.titulo}
          </h4>
        </div>
        <GripVertical size={14} className="text-muted/30 group-hover:text-muted/60 shrink-0 mt-0.5" />
      </div>

      {/* valor + probabilidad */}
      <div className="flex items-center justify-between mt-2.5">
        {op.valor_estimado > 0 ? (
          <span className="inline-flex items-center gap-1 text-[12px] font-semibold text-success tabular-nums">
            <DollarSign size={12} />{new Intl.NumberFormat('es-AR', { maximumFractionDigits: 0 }).format(op.valor_estimado)}
          </span>
        ) : <span />}
        {op.probabilidad > 0 && <span className="chip-accent !py-0.5">{op.probabilidad}%</span>}
      </div>

      {/* contacto */}
      {(op.contacto_nombre || op.contacto_email) && (
        <div className="flex items-center gap-2 mt-2 pt-2 border-t border-neutral-200/70 dark:border-slate-700/60 text-[10.5px] text-muted">
          {op.contacto_nombre && <span className="truncate">{op.contacto_nombre}</span>}
          {op.contacto_email && <Mail size={10} className="shrink-0" />}
          {op.contacto_telefono && <Phone size={10} className="shrink-0" />}
        </div>
      )}

      {/* convertir a proyecto */}
      {ganado && !op.proyecto_id && (
        <button
          onClick={(e) => { e.stopPropagation(); onConvertir() }}
          className="btn-success w-full mt-2.5 !py-1.5 !text-[12px]"
        >
          <Rocket size={13} /> Convertir a proyecto
        </button>
      )}
      {op.proyecto_id && (
        <div className="chip-success w-full justify-center mt-2.5">✓ Proyecto vinculado</div>
      )}
    </div>
  )
}

// ── Create / Edit modal ───────────────────────────────────────────────────────
const EMPTY = {
  empresa: '', titulo: '', contacto_nombre: '', contacto_email: '', contacto_telefono: '',
  descripcion: '', etapa: 'lead', valor_estimado: '', probabilidad: '',
  responsable: '', proxima_accion: '', fecha_cierre_estimada: '',
}

function OppModal({ op, onClose, onSaved }) {
  const editing = !!op
  const [form, setForm] = useState(editing ? { ...EMPTY, ...op,
    valor_estimado: op.valor_estimado || '', probabilidad: op.probabilidad || '',
    fecha_cierre_estimada: op.fecha_cierre_estimada || '' } : EMPTY)
  const [saving, setSaving] = useState(false)

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const submit = async (e) => {
    e.preventDefault()
    if (!form.empresa.trim() || !form.titulo.trim()) {
      toast.error('Empresa y título son obligatorios'); return
    }
    const valor = parseFloat(form.valor_estimado)
    const prob = parseInt(form.probabilidad, 10)
    if (form.valor_estimado !== '' && !Number.isFinite(valor)) {
      toast.error('El valor estimado debe ser numérico'); return
    }
    setSaving(true)
    const payload = {
      ...form,
      valor_estimado: Number.isFinite(valor) ? valor : 0,
      probabilidad: Number.isFinite(prob) ? prob : 0,
      fecha_cierre_estimada: form.fecha_cierre_estimada || null,
    }
    try {
      if (editing) await api.patch(`/api/crm/oportunidades/${op.id}`, payload)
      else await api.post('/api/crm/oportunidades', payload)
      toast.success(editing ? 'Oportunidad actualizada' : 'Oportunidad creada')
      onSaved()
    } catch (err) {
      if (!err?.handled) toast.error('No se pudo guardar')
    } finally {
      setSaving(false)
    }
  }

  const eliminar = async () => {
    if (!confirm('¿Eliminar esta oportunidad?')) return
    try {
      await api.delete(`/api/crm/oportunidades/${op.id}`)
      toast.success('Eliminada'); onSaved()
    } catch (e) { toast.error(e.response?.data?.detail || 'No se pudo eliminar') }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-primary/40 dark:bg-black/60 backdrop-blur-sm animate-fade-in"
         onClick={onClose}>
      <div className="card w-full max-w-lg max-h-[90vh] overflow-y-auto p-6 animate-scale-in shadow-lift"
           onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-xl font-display font-bold tracking-tight text-primary dark:text-slate-50">
            {editing ? 'Editar oportunidad' : 'Nueva oportunidad'}
          </h2>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-neutral-200/70 dark:hover:bg-slate-700 text-muted">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={submit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Empresa *</label>
              <input className="input" value={form.empresa} onChange={set('empresa')} autoFocus />
            </div>
            <div>
              <label className="label">Etapa</label>
              <select className="input" value={form.etapa} onChange={set('etapa')}>
                {ETAPAS.map(e => <option key={e.key} value={e.key}>{e.label}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="label">Título / oportunidad *</label>
            <input className="input" value={form.titulo} onChange={set('titulo')} />
          </div>

          <div>
            <label className="label">Descripción</label>
            <textarea className="textarea" rows={2} value={form.descripcion} onChange={set('descripcion')} />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Valor estimado (USD)</label>
              <input className="input" type="number" min="0" value={form.valor_estimado} onChange={set('valor_estimado')} />
            </div>
            <div>
              <label className="label">Probabilidad (%)</label>
              <input className="input" type="number" min="0" max="100" value={form.probabilidad} onChange={set('probabilidad')} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Contacto</label>
              <input className="input" value={form.contacto_nombre} onChange={set('contacto_nombre')} />
            </div>
            <div>
              <label className="label">Teléfono</label>
              <input className="input" value={form.contacto_telefono} onChange={set('contacto_telefono')} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Email</label>
              <input className="input" type="email" value={form.contacto_email} onChange={set('contacto_email')} />
            </div>
            <div>
              <label className="label">Cierre estimado</label>
              <input className="input" type="date" value={form.fecha_cierre_estimada} onChange={set('fecha_cierre_estimada')} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Responsable</label>
              <input className="input" value={form.responsable} onChange={set('responsable')} />
            </div>
            <div>
              <label className="label">Próxima acción</label>
              <input className="input" value={form.proxima_accion} onChange={set('proxima_accion')} />
            </div>
          </div>

          <div className="flex items-center justify-between gap-3 pt-2">
            {editing
              ? <button type="button" onClick={eliminar} className="btn-danger"><Trash2 size={14} /> Eliminar</button>
              : <span />}
            <div className="flex gap-2">
              <button type="button" onClick={onClose} className="btn-ghost">Cancelar</button>
              <button type="submit" disabled={saving} className="btn-accent">
                {saving ? 'Guardando…' : editing ? 'Guardar' : 'Crear'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}
