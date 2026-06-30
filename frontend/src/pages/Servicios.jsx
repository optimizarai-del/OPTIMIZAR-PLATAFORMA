import { useEffect, useMemo, useState } from 'react'
import { Plus, Package, Pencil, Trash2, X, Save, Check, ChevronRight, ChevronDown, Layers, GitBranch, List } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'
import { SkeletonRow } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const VACIO = { nombre: '', categoria: '', descripcion: '', capacidades: '', base_referencia: '', activo: true }

export default function Servicios() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [editando, setEditando] = useState(null)   // id en edición, 'nuevo', o null
  const [form, setForm] = useState(VACIO)
  const [saving, setSaving] = useState(false)
  const [vista, setVista] = useState('arbol')              // 'arbol' | 'lista'
  const [catCerradas, setCatCerradas] = useState(() => new Set())
  const [svcAbiertos, setSvcAbiertos] = useState(() => new Set())

  // Capacidades (texto) → items individuales (las hojas del árbol)
  const splitCaps = (txt) => (txt || '').split(/[\n;,•·]+/).map(t => t.trim()).filter(Boolean)
  // Agrupado macro→micro: categoría → servicios
  const porCategoria = useMemo(() => {
    const g = {}
    for (const s of items) {
      const cat = ((s.categoria || '').trim()) || 'Sin categoría'
      ;(g[cat] = g[cat] || []).push(s)
    }
    return Object.entries(g).sort((a, b) => a[0].localeCompare(b[0]))
  }, [items])
  const catOpen = (cat) => !catCerradas.has(cat)   // categorías abiertas por defecto
  const toggleCat = (cat) => setCatCerradas(p => { const n = new Set(p); n.has(cat) ? n.delete(cat) : n.add(cat); return n })
  const toggleSvc = (id) => setSvcAbiertos(p => { const n = new Set(p); n.has(id) ? n.delete(id) : n.add(id); return n })
  const expandirTodo = () => { setCatCerradas(new Set()); setSvcAbiertos(new Set(items.map(s => s.id))) }
  const colapsarTodo = () => { setCatCerradas(new Set(porCategoria.map(([c]) => c))); setSvcAbiertos(new Set()) }

  const load = () => {
    api.get('/api/servicios')
      .then(r => setItems(r.data))
      .catch(() => toast.error('No se pudieron cargar los servicios.'))
      .finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const abrirNuevo = () => { setForm(VACIO); setEditando('nuevo') }
  const abrirEdicion = s => {
    setForm({
      nombre: s.nombre || '', categoria: s.categoria || '', descripcion: s.descripcion || '',
      capacidades: s.capacidades || '', base_referencia: s.base_referencia || '', activo: s.activo,
    })
    setEditando(s.id)
  }
  const cerrar = () => { setEditando(null); setForm(VACIO) }

  const guardar = async e => {
    e.preventDefault()
    if (!form.nombre.trim()) { toast.error('El nombre es obligatorio'); return }
    setSaving(true)
    try {
      if (editando === 'nuevo') {
        await api.post('/api/servicios', form)
        toast.success('Servicio creado')
      } else {
        await api.patch(`/api/servicios/${editando}`, form)
        toast.success('Servicio actualizado')
      }
      cerrar()
      load()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'No se pudo guardar')
    } finally {
      setSaving(false)
    }
  }

  const eliminar = async (s) => {
    if (!confirm(`¿Eliminar el servicio "${s.nombre}"?`)) return
    try {
      await api.delete(`/api/servicios/${s.id}`)
      toast.success('Servicio eliminado')
      load()
    } catch {
      toast.error('No se pudo eliminar')
    }
  }

  const toggleActivo = async (s) => {
    try {
      await api.patch(`/api/servicios/${s.id}`, { activo: !s.activo })
      load()
    } catch {
      toast.error('No se pudo cambiar el estado')
    }
  }

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Comercial</div>
        <div className="flex items-end justify-between flex-wrap gap-4">
          <div>
            <h1 className="hero-title text-5xl md:text-6xl mb-3">Nuestros Servicios.</h1>
            <p className="hero-sub">Catálogo de lo que OPTIMIZAR puede ofrecer hoy. La IA lo usa para evaluar requerimientos nuevos.</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex rounded-xl border border-border overflow-hidden text-[12px] font-medium">
              <button onClick={() => setVista('arbol')}
                className={`flex items-center gap-1.5 px-3 py-2 transition-colors ${vista === 'arbol' ? 'bg-primary text-neutral-50' : 'text-muted hover:bg-neutral-100 dark:hover:bg-slate-800'}`}>
                <GitBranch size={13} /> Árbol
              </button>
              <button onClick={() => setVista('lista')}
                className={`flex items-center gap-1.5 px-3 py-2 transition-colors ${vista === 'lista' ? 'bg-primary text-neutral-50' : 'text-muted hover:bg-neutral-100 dark:hover:bg-slate-800'}`}>
                <List size={13} /> Lista
              </button>
            </div>
            <button onClick={abrirNuevo} className="btn-accent">
              <Plus size={14} /> Nuevo servicio
            </button>
          </div>
        </div>
      </header>

      {/* Form de alta/edición */}
      {editando !== null && (
        <form onSubmit={guardar} className="card p-7 mb-8 animate-fade-in">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-bold text-lg tracking-tight">
              {editando === 'nuevo' ? 'Nuevo servicio' : 'Editar servicio'}
            </h2>
            <button type="button" onClick={cerrar} className="btn-ghost text-muted"><X size={16} /></button>
          </div>
          <div className="space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Nombre *</label>
                <input className="input" required placeholder="Ej: Agente WhatsApp por rubro" value={form.nombre} onChange={set('nombre')} />
              </div>
              <div>
                <label className="label">Categoría</label>
                <input className="input" placeholder="Agentes, Automatización, Dashboards..." value={form.categoria} onChange={set('categoria')} />
              </div>
            </div>
            <div>
              <label className="label">Descripción (qué resuelve)</label>
              <textarea className="textarea" rows={2} placeholder="En una o dos frases, qué problema resuelve este servicio."
                value={form.descripcion} onChange={set('descripcion')} />
            </div>
            <div>
              <label className="label">Capacidades (qué hace concretamente)</label>
              <textarea className="textarea" rows={3} placeholder="Tecnologías, integraciones y funciones. Esto es lo que la IA compara contra cada requerimiento."
                value={form.capacidades} onChange={set('capacidades')} />
            </div>
            <div className="grid grid-cols-2 gap-4 items-end">
              <div>
                <label className="label">Proyecto base / referencia</label>
                <input className="input" placeholder="Ej: Larrañaga, SONNER..." value={form.base_referencia} onChange={set('base_referencia')} />
              </div>
              <label className="flex items-center gap-3 cursor-pointer pb-2">
                <div className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-all ${
                  form.activo ? 'border-accent bg-accent' : 'border-border'
                }`}>
                  {form.activo && <Check size={11} className="text-white" />}
                </div>
                <input type="checkbox" className="hidden" checked={form.activo}
                  onChange={e => setForm(f => ({ ...f, activo: e.target.checked }))} />
                <span className="text-[13px]">Activo (disponible para ofrecer)</span>
              </label>
            </div>
          </div>
          <div className="flex gap-3 mt-7">
            <button type="button" onClick={cerrar} className="btn-secondary flex-1">Cancelar</button>
            <button type="submit" disabled={saving} className="btn-accent flex-1 disabled:opacity-50">
              <Save size={14} /> {saving ? 'Guardando...' : 'Guardar servicio'}
            </button>
          </div>
        </form>
      )}

      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <SkeletonRow key={i} />)}</div>
      ) : items.length === 0 ? (
        <EmptyState
          icon={Package}
          title="No hay servicios cargados todavía"
          description="Cargá el primer servicio que OPTIMIZAR puede ofrecer."
          action={abrirNuevo}
          actionLabel="+ Cargar primer servicio"
        />
      ) : vista === 'lista' ? (
        <div className="space-y-3">
          {items.map(s => (
            <div key={s.id} className={`card p-5 card-hover ${!s.activo ? 'opacity-60' : ''}`}>
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <span className="font-bold text-[16px] tracking-tight">{s.nombre}</span>
                    {s.categoria && <span className="chip-primary">{s.categoria}</span>}
                    <button onClick={() => toggleActivo(s)}
                      className={s.activo ? 'chip-success' : 'chip-muted'} title="Click para cambiar">
                      {s.activo ? 'Activo' : 'Inactivo'}
                    </button>
                  </div>
                  {s.descripcion && <div className="text-[13px] text-muted mb-1">{s.descripcion}</div>}
                  {s.capacidades && <div className="text-[12px] text-muted/80"><span className="font-medium">Capacidades:</span> {s.capacidades}</div>}
                  {s.base_referencia && <div className="text-[12px] text-muted/70 mt-1">Base: {s.base_referencia}</div>}
                </div>
                <div className="flex gap-2">
                  <button onClick={() => abrirEdicion(s)} className="btn-ghost text-muted" title="Editar"><Pencil size={14} /></button>
                  <button onClick={() => eliminar(s)} className="btn-ghost text-danger" title="Eliminar"><Trash2 size={14} /></button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4 gap-3 flex-wrap">
            <div className="text-[12px] text-muted">
              Mapa de servicios: de lo <span className="font-semibold">macro</span> (categoría) a lo <span className="font-semibold">micro</span> (capacidad). Tocá para desplegar.
            </div>
            <div className="flex gap-2 text-[11px] shrink-0">
              <button onClick={expandirTodo} className="text-accent-600 hover:underline">Expandir todo</button>
              <span className="text-muted/40">·</span>
              <button onClick={colapsarTodo} className="text-accent-600 hover:underline">Colapsar todo</button>
            </div>
          </div>
          <div className="space-y-1">
            {porCategoria.map(([cat, servicios]) => (
              <div key={cat}>
                {/* Nivel 1 — Categoría (macro) */}
                <button onClick={() => toggleCat(cat)}
                  className="w-full flex items-center gap-2 py-1.5 px-1 text-left rounded-lg hover:bg-neutral-100 dark:hover:bg-slate-800 transition-colors">
                  {catOpen(cat) ? <ChevronDown size={15} className="text-accent shrink-0" /> : <ChevronRight size={15} className="text-muted shrink-0" />}
                  <Layers size={15} className="text-accent shrink-0" />
                  <span className="font-bold text-[14px] tracking-tight">{cat}</span>
                  <span className="chip-muted ml-1">{servicios.length}</span>
                </button>

                {catOpen(cat) && (
                  <div className="ml-[10px] pl-4 border-l-2 border-border space-y-0.5 py-0.5">
                    {servicios.map(s => {
                      const caps = splitCaps(s.capacidades)
                      const tieneHijos = caps.length > 0 || !!s.descripcion
                      const open = svcAbiertos.has(s.id)
                      return (
                        <div key={s.id}>
                          {/* Nivel 2 — Servicio */}
                          <button onClick={() => { if (tieneHijos) toggleSvc(s.id) }}
                            className={`w-full flex items-center gap-2 py-1 px-1 text-left rounded-lg hover:bg-neutral-100 dark:hover:bg-slate-800 transition-colors ${!s.activo ? 'opacity-55' : ''}`}>
                            {tieneHijos
                              ? (open ? <ChevronDown size={14} className="text-muted shrink-0" /> : <ChevronRight size={14} className="text-muted shrink-0" />)
                              : <span className="w-[14px] shrink-0" />}
                            <Package size={13} className="text-accent/70 shrink-0" />
                            <span className="font-semibold text-[13px]">{s.nombre}</span>
                            {!s.activo && <span className="chip-muted !text-[9px]">inactivo</span>}
                            {s.base_referencia && <span className="text-[10px] text-muted/60">· base: {s.base_referencia}</span>}
                          </button>

                          {open && tieneHijos && (
                            <div className="ml-[10px] pl-4 border-l-2 border-border/50 py-0.5 space-y-0.5">
                              {s.descripcion && <div className="text-[12px] text-muted italic py-0.5">{s.descripcion}</div>}
                              {/* Nivel 3 — Capacidades (micro) */}
                              {caps.map((c, i) => (
                                <div key={i} className="flex items-start gap-2 py-0.5">
                                  <span className="w-1.5 h-1.5 rounded-full bg-accent/50 mt-[7px] shrink-0" />
                                  <span className="text-[12px] text-primary dark:text-slate-200">{c}</span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
