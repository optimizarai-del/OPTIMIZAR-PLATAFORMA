import { useEffect, useState } from 'react'
import { Plus, Package, Pencil, Trash2, X, Save, Check } from 'lucide-react'
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
          <button onClick={abrirNuevo} className="btn-accent">
            <Plus size={14} /> Nuevo servicio
          </button>
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
      ) : (
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
      )}
    </div>
  )
}
