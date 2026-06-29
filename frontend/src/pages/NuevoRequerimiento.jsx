import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save, Sparkles, CheckCircle2, AlertTriangle } from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'

const HERRAMIENTAS_OPT = [
  'Excel / Google Sheets',
  'WhatsApp / Telegram',
  'Correo Electrónico (Gmail / Outlook)',
  'Trello / Asana / ClickUp',
]

const ACCESO_OPT = [
  'Tienen API propia documentada.',
  'Entran con usuario y contraseña genéricos/compartidos.',
  'Cada empleado entra con sus credenciales personales (Ej. Clave Fiscal individual).',
  'No saben / A confirmar por Desarrollo.',
]

export default function NuevoRequerimiento() {
  const nav = useNavigate()
  const [form, setForm] = useState({
    nombre_cliente: '',
    sector: '',
    personas_reunion: '',
    sistemas_core: '',
    herramientas: [],
    uso_ia: '',
    tipos_acceso: [],
    estado_bd: '',
    nombre_proceso: '',
    trigger_proceso: '',
    pasos_manuales: '',
    volumen_proceso: '',
    tiempo_por_proceso: '',
    responsable_comercial: '',
    fecha_entrega: '',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [resultado, setResultado] = useState(null)   // requerimiento creado + análisis
  const [herramientaOtro, setHerramientaOtro] = useState('')  // campo "Otro" (controlado)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  // El "Otro" de herramientas: reconstruye el array con las predefinidas tildadas + el texto libre.
  const setOtroHerramienta = (texto) => {
    setHerramientaOtro(texto)
    setForm(f => {
      const predefinidas = f.herramientas.filter(h => HERRAMIENTAS_OPT.includes(h))
      return { ...f, herramientas: texto.trim() ? [...predefinidas, texto.trim()] : predefinidas }
    })
  }

  const toggleArr = (key, val) => setForm(f => ({
    ...f,
    [key]: f[key].includes(val)
      ? f[key].filter(x => x !== val)
      : [...f[key], val]
  }))

  const handle = async e => {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      const { data } = await api.post('/api/requerimientos', {
        ...form,
        fecha_entrega: form.fecha_entrega || null,
      })
      toast.success(`Requerimiento de ${form.nombre_cliente} registrado`)
      setResultado(data)   // mostramos el análisis IA antes de salir
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (err) {
      const msg = err.response?.data?.detail || 'Error al guardar. Verificá los datos.'
      setError(msg)
      toast.error(msg)
    } finally {
      setSaving(false)
    }
  }

  if (resultado) {
    const cubierto = resultado.analisis_estado === 'cubierto'
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        <button onClick={() => nav('/requerimientos')} className="btn-ghost mb-6 -ml-2 text-muted">
          <ArrowLeft size={14} /> Requerimientos
        </button>
        <div className="card p-8">
          <div className="flex items-center gap-2 text-accent text-[12px] font-semibold uppercase tracking-wide mb-4">
            <Sparkles size={14} /> Análisis automático de cobertura
          </div>
          <h1 className="text-2xl font-bold tracking-tight mb-1">{resultado.nombre_cliente}</h1>
          {resultado.nombre_proceso && <p className="text-muted text-[14px] mb-6">{resultado.nombre_proceso}</p>}

          {cubierto ? (
            <div className="rounded-2xl p-5 bg-success/5 border border-success/25">
              <div className="flex items-center gap-2.5 mb-2">
                <CheckCircle2 size={20} className="text-success" />
                <span className="font-bold text-success text-[15px]">
                  Cubierto por: {resultado.servicio_match_nombre || 'un servicio existente'}
                </span>
                {typeof resultado.analisis_confianza === 'number' && (
                  <span className="chip-success">{resultado.analisis_confianza}% confianza</span>
                )}
              </div>
              {resultado.analisis_justificacion && (
                <p className="text-[13px] text-muted">{resultado.analisis_justificacion}</p>
              )}
            </div>
          ) : (
            <div className="rounded-2xl p-5 bg-warn/5 border border-warn/30">
              <div className="flex items-center gap-2.5 mb-2">
                <AlertTriangle size={20} className="text-warn" />
                <span className="font-bold text-warn text-[15px]">Consultar con área de desarrollo</span>
              </div>
              <p className="text-[13px] text-muted">
                {resultado.analisis_justificacion || 'Ningún servicio del catálogo cubre este requerimiento.'}
              </p>
            </div>
          )}

          <div className="flex gap-3 mt-7">
            <button onClick={() => nav('/requerimientos')} className="btn-accent flex-1">
              Ver en Requerimientos
            </button>
            <button onClick={() => { setResultado(null); setForm(f => ({ ...f, nombre_cliente: '', nombre_proceso: '' })) }}
              className="btn-secondary flex-1">
              Cargar otro
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <button onClick={() => nav('/requerimientos')} className="btn-ghost mb-6 -ml-2 text-muted">
        <ArrowLeft size={14} /> Requerimientos
      </button>

      <header className="mb-10">
        <div className="hero-eyebrow">Optimizar IA — Traspaso Comercial a Desarrollo</div>
        <h1 className="hero-title text-4xl md:text-5xl mb-3">Cargar Requerimiento.</h1>
        <p className="hero-sub text-base">
          Documento obligatorio. Desarrollo no inicia evaluación técnica ni emite presupuesto si faltan datos de volumen o detalle de accesos.
        </p>
      </header>

      <form onSubmit={handle} className="space-y-8">

        {/* Sección 1 */}
        <Section num="1" title="Información General">
          <div>
            <label className="label">Nombre del Cliente / Empresa *</label>
            <input className="input" required placeholder="Empresa S.A." value={form.nombre_cliente} onChange={set('nombre_cliente')} />
          </div>
          <div>
            <label className="label">Sector / Industria</label>
            <input className="input" placeholder="Ej: Contabilidad, Logística, Retail..." value={form.sector} onChange={set('sector')} />
          </div>
          <div>
            <label className="label">Personas presentes en la reunión (Tomadores de decisión)</label>
            <input className="input" placeholder="Ej: Dr. López (socio), Lic. Ramírez (admin)" value={form.personas_reunion} onChange={set('personas_reunion')} />
          </div>
        </Section>

        {/* Sección 2 */}
        <Section num="2" title="Ecosistema Tecnológico (Stack Actual)">
          <div>
            <label className="label">Sistemas Core / ERPs actuales (Ej. Holistor, Onvio, Tango, SAP)</label>
            <input className="input" placeholder="Ej: Tango + Holistor" value={form.sistemas_core} onChange={set('sistemas_core')} />
          </div>
          <div>
            <label className="label">Herramientas cotidianas de soporte</label>
            <div className="space-y-2 mt-2">
              {HERRAMIENTAS_OPT.map(h => (
                <CheckItem key={h} label={h}
                  checked={form.herramientas.includes(h)}
                  onChange={() => toggleArr('herramientas', h)} />
              ))}
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded border-border border-2 flex-shrink-0" />
                <input className="input !py-2" placeholder="Otro: ..."
                  value={herramientaOtro}
                  onChange={e => setOtroHerramienta(e.target.value)} />
              </div>
            </div>
          </div>
          <div>
            <label className="label">Uso actual de IA o automatizaciones</label>
            <input className="input" placeholder="Ej: ChatGPT Plus, Claude, Zapier..." value={form.uso_ia} onChange={set('uso_ia')} />
          </div>
        </Section>

        {/* Sección 3 */}
        <Section num="3" title="Restricciones Técnicas y Accesos">
          <div>
            <label className="label">Tipos de Acceso a los sistemas</label>
            <div className="space-y-2 mt-2">
              {ACCESO_OPT.map(a => (
                <CheckItem key={a} label={a}
                  checked={form.tipos_acceso.includes(a)}
                  onChange={() => toggleArr('tipos_acceso', a)} />
              ))}
            </div>
          </div>
          <div>
            <label className="label">Estado de la Base de Datos / Información</label>
            <textarea className="textarea" rows={2}
              placeholder="¿Está centralizada o en Excels sueltos?"
              value={form.estado_bd} onChange={set('estado_bd')} />
          </div>
        </Section>

        {/* Sección 4 */}
        <Section num="4" title="El Dolor (Proceso Principal a Automatizar)">
          <div>
            <label className="label">Nombre del proceso *</label>
            <input className="input" required placeholder="Ej: Emisión de facturas electrónicas AFIP" value={form.nombre_proceso} onChange={set('nombre_proceso')} />
          </div>
          <div>
            <label className="label">El "Trigger" / Gatillo</label>
            <input className="input" placeholder='Ej: "Llega un mail con adjunto"' value={form.trigger_proceso} onChange={set('trigger_proceso')} />
          </div>
          <div>
            <label className="label">Paso a paso manual actual</label>
            <textarea className="textarea" rows={4}
              placeholder="Describir qué clics y pantallas abre el humano hoy..."
              value={form.pasos_manuales} onChange={set('pasos_manuales')} />
          </div>
        </Section>

        {/* Sección 5 */}
        <Section num="5" title="Calculadora de Impacto (Métricas para el ROI)">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Volumen del proceso *</label>
              <input className="input" required placeholder="Ej: ~120 facturas/mes" value={form.volumen_proceso} onChange={set('volumen_proceso')} />
              <p className="text-[11px] text-muted mt-1">¿Cuántas veces al mes/semana se hace esto?</p>
            </div>
            <div>
              <label className="label">Tiempo por ejecución *</label>
              <input className="input" required placeholder="Ej: 15-20 minutos" value={form.tiempo_por_proceso} onChange={set('tiempo_por_proceso')} />
              <p className="text-[11px] text-muted mt-1">¿Cuánto tarda hacer esto UNA sola vez?</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Responsable Comercial</label>
              <input className="input" placeholder="Nombre del vendedor" value={form.responsable_comercial} onChange={set('responsable_comercial')} />
            </div>
            <div>
              <label className="label">Fecha de entrega a Desarrollo</label>
              <input className="input" type="date" value={form.fecha_entrega} onChange={set('fecha_entrega')} />
            </div>
          </div>

          <div className="bg-accent/5 rounded-2xl p-4 border border-accent/20">
            <p className="text-[12px] text-accent-700 font-medium">
              Uso interno: Volumen × Tiempo = Horas totales ahorradas. Esta es la métrica para cotizar el abono mensual.
            </p>
            <p className="text-[12px] text-muted mt-1">
              A partir de la fecha de entrega, Desarrollo tiene 48hs hábiles para entregar la evaluación técnica.
            </p>
          </div>
        </Section>

        {error && <div className="text-danger text-[13px] bg-danger/5 rounded-xl px-4 py-3">{error}</div>}

        <div className="flex gap-4 pb-10">
          <button type="button" onClick={() => nav('/requerimientos')} className="btn-secondary flex-1">
            Cancelar
          </button>
          <button type="submit" disabled={saving} className="btn-accent btn-lg flex-1 disabled:opacity-50">
            <Save size={15} /> {saving ? 'Guardando...' : 'Enviar requerimiento'}
          </button>
        </div>
      </form>
    </div>
  )
}

function Section({ num, title, children }) {
  return (
    <div className="card p-7">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 rounded-xl bg-accent text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
          {num}
        </div>
        <h2 className="font-bold text-lg tracking-tight">{title}</h2>
      </div>
      <div className="space-y-5">{children}</div>
    </div>
  )
}

function CheckItem({ label, checked, onChange }) {
  return (
    <label className="flex items-start gap-3 cursor-pointer group">
      <div className={`mt-0.5 w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 transition-all ${
        checked ? 'border-accent bg-accent' : 'border-border group-hover:border-accent'
      }`}>
        {checked && <svg width="8" height="6" viewBox="0 0 8 6" fill="none"><path d="M1 3L3 5L7 1" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>}
      </div>
      <span className="text-[13px] leading-relaxed">{label}</span>
    </label>
  )
}
