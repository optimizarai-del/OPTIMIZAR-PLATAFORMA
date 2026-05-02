import { useEffect, useState } from 'react'
import { Mail, MailX, RefreshCw, CheckCircle, XCircle, Zap, Settings } from 'lucide-react'
import api from '../utils/api'
import { SkeletonRow } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'

const TIPO_LABEL = {
  tarea_asignada:        'Tarea asignada',
  cambio_estado:         'Cambio de estado',
  reasignacion:          'Reasignación',
  detalles_actualizados: 'Detalles actualizados',
  tarea_completada:      'Tarea completada',
}
const TIPO_COLOR = {
  tarea_asignada:        '#6366F1',
  cambio_estado:         '#B45309',
  reasignacion:          '#8B5CF6',
  detalles_actualizados: '#0EA5E9',
  tarea_completada:      '#059669',
}
const TIPO_ICON = {
  tarea_asignada:        '📋',
  cambio_estado:         '🔄',
  reasignacion:          '👤',
  detalles_actualizados: '✏️',
  tarea_completada:      '✅',
}

export default function Notificaciones() {
  const [notifs, setNotifs]   = useState([])
  const [stats, setStats]     = useState(null)
  const [loading, setLoading] = useState(true)
  const [soloErr, setSoloErr] = useState(false)

  const load = () => {
    setLoading(true)
    Promise.all([
      api.get(`/api/notificaciones?solo_errores=${soloErr}`),
      api.get('/api/notificaciones/stats'),
    ]).then(([n, s]) => {
      setNotifs(n.data)
      setStats(s.data)
    }).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [soloErr])

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Sistema</div>
        <div className="flex items-end justify-between flex-wrap gap-4">
          <div>
            <h1 className="hero-title text-5xl md:text-6xl mb-3">Notificaciones.</h1>
            <p className="hero-sub">Historial de emails enviados por el sistema.</p>
          </div>
          <button onClick={load} className="btn-ghost">
            <RefreshCw size={14} /> Actualizar
          </button>
        </div>
      </header>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="card p-5">
            <div className="stat-label">Total enviadas</div>
            <div className="hero-title text-4xl mt-1 text-primary dark:text-slate-50">{stats.total}</div>
          </div>
          <div className="card p-5">
            <div className="stat-label">Entregadas</div>
            <div className="hero-title text-4xl mt-1 text-success">{stats.enviadas}</div>
          </div>
          <div className="card p-5">
            <div className="stat-label">Con error</div>
            <div className="hero-title text-4xl mt-1 text-danger">{stats.errores}</div>
          </div>
        </div>
      )}

      {/* Config SMTP banner */}
      <div className="card p-5 mb-6 border-accent/30 dark:border-accent/20 bg-accent/5 dark:bg-accent/10">
        <div className="flex items-start gap-4">
          <div className="w-9 h-9 rounded-xl bg-accent/15 flex items-center justify-center flex-shrink-0">
            <Settings size={15} className="text-accent-600 dark:text-accent-400" />
          </div>
          <div className="flex-1">
            <div className="font-semibold text-[14px] text-primary dark:text-slate-100 mb-1">
              Configuración SMTP
            </div>
            <p className="text-[12px] text-muted dark:text-slate-400 leading-relaxed mb-3">
              Para activar el envío real de emails, editá <code className="bg-neutral-200 dark:bg-slate-700 px-1.5 py-0.5 rounded-md text-[11px]">backend/.env</code> y configurá:
            </p>
            <div className="grid sm:grid-cols-2 gap-2">
              {[
                ['NOTIFICATIONS_ENABLED', 'true'],
                ['SMTP_HOST', 'smtp.gmail.com'],
                ['SMTP_PORT', '587'],
                ['SMTP_USER', 'tu@gmail.com'],
                ['SMTP_PASSWORD', 'contraseña de app (16 chars)'],
                ['APP_URL', 'https://tu-dominio.com'],
              ].map(([k, v]) => (
                <div key={k} className="flex items-center gap-2 text-[11px] font-mono">
                  <span className="text-accent-600 dark:text-accent-400 font-semibold">{k}</span>
                  <span className="text-muted">=</span>
                  <span className="text-primary dark:text-slate-300">{v}</span>
                </div>
              ))}
            </div>
            <p className="text-[11px] text-muted dark:text-slate-500 mt-3">
              Gmail: activá "Verificación en dos pasos" → "Contraseñas de aplicación" → generá una para "Correo".
            </p>
          </div>
        </div>
      </div>

      {/* Filtro */}
      <div className="flex gap-2 mb-6">
        <button onClick={() => setSoloErr(false)}
          className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
            !soloErr ? 'bg-primary dark:bg-slate-100 text-white dark:text-slate-900 shadow-soft'
                     : 'bg-white dark:bg-slate-800 text-muted border border-border dark:border-slate-700 hover:bg-neutral-100 dark:hover:bg-slate-700'
          }`}>
          Todas
        </button>
        <button onClick={() => setSoloErr(true)}
          className={`px-4 py-2 rounded-full text-[13px] font-medium transition-all ${
            soloErr ? 'bg-danger/10 text-danger shadow-soft'
                    : 'bg-white dark:bg-slate-800 text-muted border border-border dark:border-slate-700 hover:bg-neutral-100 dark:hover:bg-slate-700'
          }`}>
          <XCircle size={13} className="inline mr-1" /> Solo errores
        </button>
      </div>

      {/* Lista */}
      {loading ? (
        <div className="space-y-3">
          {[1,2,3,4].map(i => <SkeletonRow key={i} />)}
        </div>
      ) : notifs.length === 0 ? (
        <EmptyState
          icon={Mail}
          title={soloErr ? 'Sin errores de envío' : 'Sin notificaciones todavía'}
          description="Las notificaciones se generan automáticamente al asignar tareas, cambiar estados o modificar detalles."
        />
      ) : (
        <div className="space-y-2">
          {notifs.map(n => (
            <NotifRow key={n.id} n={n} />
          ))}
        </div>
      )}

      {/* Leyenda de eventos */}
      <div className="card p-6 mt-8">
        <div className="hero-eyebrow text-[10px] mb-4">Eventos que generan notificaciones</div>
        <div className="grid sm:grid-cols-2 gap-3">
          {Object.entries(TIPO_LABEL).map(([tipo, label]) => (
            <div key={tipo} className="flex items-center gap-3">
              <span className="text-lg">{TIPO_ICON[tipo]}</span>
              <div>
                <div className="text-[13px] font-medium text-primary dark:text-slate-100">{label}</div>
                <div className="text-[11px] text-muted dark:text-slate-500">
                  {tipo === 'tarea_asignada'        && 'Al crear una tarea con asignado'}
                  {tipo === 'cambio_estado'         && 'Al cambiar el estado de una tarea'}
                  {tipo === 'reasignacion'          && 'Al cambiar el responsable de una tarea'}
                  {tipo === 'detalles_actualizados' && 'Al modificar título, descripción o prioridad'}
                  {tipo === 'tarea_completada'      && 'Al marcar una tarea como completada'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function NotifRow({ n }) {
  const [expanded, setExpanded] = useState(false)
  const color = TIPO_COLOR[n.tipo] ?? '#6366F1'
  const fecha = new Date(n.created_at).toLocaleString('es-AR', {
    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
  })

  return (
    <div className="card overflow-hidden">
      <div className="p-4 flex items-center gap-4 cursor-pointer hover:bg-neutral-50 dark:hover:bg-slate-700/40 transition-colors"
        onClick={() => setExpanded(e => !e)}>
        {/* Icono tipo */}
        <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 text-base"
          style={{ backgroundColor: `${color}18` }}>
          {TIPO_ICON[n.tipo] ?? '📧'}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="chip text-[11px] font-semibold"
              style={{ backgroundColor: `${color}15`, color }}>
              {TIPO_LABEL[n.tipo] ?? n.tipo}
            </span>
            <span className="text-[13px] font-medium text-primary dark:text-slate-100 truncate">
              {n.asunto}
            </span>
          </div>
          <div className="flex items-center gap-3 mt-1 text-[11px] text-muted dark:text-slate-500">
            <span>→ {n.destinatario_email}</span>
            <span>{fecha}</span>
          </div>
        </div>

        {/* Estado */}
        <div className="flex-shrink-0">
          {n.enviado
            ? <CheckCircle size={16} className="text-success" />
            : <XCircle size={16} className="text-danger" />
          }
        </div>
      </div>

      {/* Detalle expandido */}
      {expanded && (
        <div className="px-4 pb-4 border-t border-border dark:border-slate-700">
          {n.error && (
            <div className="mt-3 p-3 bg-danger/5 dark:bg-danger/10 rounded-xl border border-danger/20">
              <div className="text-[11px] font-semibold text-danger mb-1 uppercase tracking-wider">
                Error de envío
              </div>
              <code className="text-[12px] text-danger/80">{n.error}</code>
            </div>
          )}
          {!n.error && !n.enviado && (
            <div className="mt-3 p-3 bg-neutral-100 dark:bg-slate-700/40 rounded-xl">
              <p className="text-[12px] text-muted">
                Notificaciones desactivadas (NOTIFICATIONS_ENABLED=false).
                La notificación fue registrada pero no enviada por email.
              </p>
            </div>
          )}
          {n.enviado && (
            <div className="mt-3 p-3 bg-success/5 dark:bg-success/10 rounded-xl border border-success/20">
              <p className="text-[12px] text-success font-medium">
                Email entregado correctamente a {n.destinatario_email}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
