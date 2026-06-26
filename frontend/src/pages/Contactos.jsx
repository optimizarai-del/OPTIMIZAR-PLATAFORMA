import { useEffect, useState } from 'react'
import { Users, Mail, Phone, Tag, ArrowUpRight, Trash2, MessageSquare } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'
import { SkeletonRow } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const ESTADO = {
  nuevo:      { label: 'Nuevo',       chip: 'chip-muted' },
  escrito:    { label: 'Mensaje listo', chip: 'chip-accent' },
  contactado: { label: 'Contactado',  chip: 'chip-warn' },
  respondido: { label: 'Respondió',   chip: 'chip-success' },
  rebote:     { label: 'Rebote',      chip: 'chip-danger' },
  baja:       { label: 'Baja',        chip: 'chip-muted' },
}

const FILTROS = [
  { label: 'Todos', value: '' },
  { label: 'Nuevos', value: 'nuevo' },
  { label: 'Contactados', value: 'contactado' },
  { label: 'Respondieron', value: 'respondido' },
]

export default function Contactos() {
  const [items, setItems] = useState([])
  const [filtro, setFiltro] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    api.get('/api/crm/contactos')
      .then(r => setItems(r.data))
      .catch(() => toast.error('No se pudieron cargar los contactos.'))
      .finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const promover = async (c) => {
    try {
      await api.post(`/api/crm/contactos/${c.id}/promover`)
      toast.success(`${c.empresa} subió al pipeline`)
      load()
    } catch {
      toast.error('No se pudo promover')
    }
  }

  const eliminar = async (c) => {
    if (!confirm(`¿Eliminar el contacto "${c.empresa}"?`)) return
    try {
      await api.delete(`/api/crm/contactos/${c.id}`)
      toast.success('Contacto eliminado')
      load()
    } catch {
      toast.error('No se pudo eliminar')
    }
  }

  const filtrados = filtro ? items.filter(c => c.estado === filtro) : items

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <header className="mb-8">
        <div className="hero-eyebrow">Comercial</div>
        <h1 className="hero-title text-5xl md:text-6xl mb-3">Contactos.</h1>
        <p className="hero-sub">Base de prospección. Los agentes dejan acá los leads. Suben al pipeline cuando responden.</p>
      </header>

      <div className="flex gap-2 mb-8 flex-wrap">
        {FILTROS.map(f => {
          const count = f.value ? items.filter(c => c.estado === f.value).length : items.length
          return (
            <button key={f.value} onClick={() => setFiltro(f.value)}
              className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
                filtro === f.value ? 'bg-primary text-neutral-50 shadow-soft'
                  : 'bg-white text-muted hover:bg-neutral-200/70 border border-border'
              }`}>
              {f.label} <span className="ml-1 opacity-60">({count})</span>
            </button>
          )
        })}
      </div>

      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <SkeletonRow key={i} />)}</div>
      ) : filtrados.length === 0 ? (
        <EmptyState
          icon={Users}
          title={filtro ? `Sin contactos en estado "${ESTADO[filtro]?.label}"` : 'No hay contactos todavía'}
          description="Los agentes de prospección van a dejar acá los leads que encuentren y contacten."
        />
      ) : (
        <div className="space-y-3">
          {filtrados.map(c => {
            const est = ESTADO[c.estado] || ESTADO.nuevo
            return (
              <div key={c.id} className="card p-5 card-hover">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span className="font-bold text-[16px] tracking-tight">{c.empresa}</span>
                      <span className={est.chip}>{est.label}</span>
                      {c.origen && (
                        <span className="chip-primary flex items-center gap-1"><Tag size={10} /> {c.origen}</span>
                      )}
                    </div>
                    {c.nombre && <div className="text-[13px] text-muted">{c.nombre}</div>}
                    <div className="flex items-center gap-4 mt-2 text-[12px] text-muted flex-wrap">
                      {c.email && <span className="flex items-center gap-1"><Mail size={11} /> {c.email}</span>}
                      {c.telefono && <span className="flex items-center gap-1"><Phone size={11} /> {c.telefono}</span>}
                    </div>
                    {c.info && <div className="text-[12px] text-muted mt-2">{c.info}</div>}
                    {c.disparador && <div className="text-[12px] text-accent-700 mt-1">Disparador: {c.disparador}</div>}
                    {c.respuesta_recibida && (
                      <div className="text-[12px] mt-2 bg-success/5 border border-success/20 rounded-xl px-3 py-2 flex gap-2">
                        <MessageSquare size={13} className="text-success shrink-0 mt-0.5" />
                        <span>{c.respuesta_recibida}</span>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-2 shrink-0">
                    {!c.oportunidad_id && (
                      <button onClick={() => promover(c)} className="btn-accent !py-1.5 !px-3 text-[12px]" title="Subir al pipeline">
                        <ArrowUpRight size={13} /> Al pipeline
                      </button>
                    )}
                    {c.oportunidad_id && <span className="chip-success self-center">En pipeline ✓</span>}
                    <button onClick={() => eliminar(c)} className="btn-ghost text-danger" title="Eliminar"><Trash2 size={14} /></button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
