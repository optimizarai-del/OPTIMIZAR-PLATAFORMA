import { useEffect, useState, useCallback, useRef } from 'react'
import {
  Megaphone, TrendingUp, MousePointerClick, Eye, DollarSign, Target,
  Lightbulb, CheckCircle2, XCircle, Loader2, RefreshCw, Plug, AlertTriangle,
  ArrowUpRight, Sparkles,
} from 'lucide-react'
import api from '../utils/api'
import { toast } from '../utils/toast'

const RANGOS = [7, 14, 30]

const fmtMoneda = (n, mon = 'ARS') =>
  new Intl.NumberFormat('es-AR', { style: 'currency', currency: mon, maximumFractionDigits: 0 })
    .format(n || 0)
const fmtNum = (n) => new Intl.NumberFormat('es-AR').format(Math.round(n || 0))

const SEV = {
  alta:  'chip-danger',
  media: 'chip-accent',
  baja:  'chip-muted',
}
const TIPO_LABEL = {
  escalar: 'Escalar', pausar: 'Pausar', presupuesto: 'Presupuesto',
  creativo: 'Creativo', audiencia: 'Audiencia', ajuste: 'Ajuste',
}

export default function Marketing() {
  const [dias, setDias] = useState(14)
  const [ov, setOv] = useState(null)
  const [camps, setCamps] = useState([])
  const [recos, setRecos] = useState([])
  const [loading, setLoading] = useState(true)
  const aliveRef = useRef(true)

  const cargar = useCallback((d) => {
    setLoading(true)
    Promise.all([
      api.get(`/api/ads/overview?dias=${d}`),
      api.get(`/api/ads/campaigns?dias=${d}`),
      api.get('/api/ads/recommendations'),
    ]).then(([o, c, r]) => {
      if (!aliveRef.current) return
      setOv(o.data); setCamps(c.data); setRecos(r.data)
    }).catch((err) => {
      if (!err?.handled) toast.error('No se pudieron cargar las métricas de Ads.')
    }).finally(() => { if (aliveRef.current) setLoading(false) })
  }, [])

  useEffect(() => {
    aliveRef.current = true
    cargar(dias)
    return () => { aliveRef.current = false }
  }, [dias, cargar])

  const decidirReco = async (r, estado) => {
    try {
      const { data } = await api.patch(`/api/ads/recommendations/${r.id}?estado=${estado}`)
      setRecos(list => list.map(x => x.id === r.id ? data : x))
      toast.success(estado === 'aplicada' ? 'Marcada como aplicada' : 'Descartada')
    } catch (err) {
      if (!err?.handled) toast.error('No se pudo actualizar la recomendación.')
    }
  }

  const conectado = ov?.conectado
  const recosNuevas = recos.filter(r => r.estado === 'nueva')

  return (
    <div className="space-y-7 animate-fade-in">
      {/* ── Header ── */}
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <div className="hero-eyebrow !mb-1.5">Marketing · Performance</div>
          <h1 className="text-3xl md:text-4xl hero-title">Meta Ads</h1>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex rounded-full bg-neutral-100 dark:bg-slate-800 p-0.5">
            {RANGOS.map(d => (
              <button key={d} onClick={() => setDias(d)}
                className={`px-3 py-1.5 rounded-full text-[12px] font-medium transition-all ${
                  dias === d ? 'bg-white dark:bg-slate-700 shadow-soft text-primary dark:text-slate-100'
                             : 'text-muted hover:text-primary dark:hover:text-slate-200'}`}>
                {d}d
              </button>
            ))}
          </div>
          <button onClick={() => cargar(dias)} className="btn-ghost !rounded-full !px-3" title="Refrescar">
            <RefreshCw size={15} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* ── Estado de conexión ── */}
      <ConexionCard ov={ov} loading={loading} />

      {loading && !ov ? (
        <div className="flex items-center justify-center py-20 text-muted">
          <Loader2 className="animate-spin" size={20} />
        </div>
      ) : (
        <>
          {/* ── KPIs ── */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <Kpi icon={DollarSign} label="Gasto" value={fmtMoneda(ov?.gasto_total)} accent />
            <Kpi icon={Eye} label="Impresiones" value={fmtNum(ov?.impresiones_total)} />
            <Kpi icon={MousePointerClick} label="Clicks" value={fmtNum(ov?.clicks_total)}
                 sub={`CTR ${(ov?.ctr_prom || 0).toFixed(2)}%`} />
            <Kpi icon={Target} label="Conversiones" value={fmtNum(ov?.conversiones_total)}
                 sub={ov?.roas_prom ? `ROAS ${ov.roas_prom.toFixed(2)}x` : `CPC ${fmtMoneda(ov?.cpc_prom)}`} />
          </div>

          {/* ── Gasto en el tiempo ── */}
          <GastoChart serie={ov?.serie_gasto || []} />

          {/* ── Recomendaciones + Campañas ── */}
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
            <div className="lg:col-span-3">
              <CampañasTabla camps={camps} />
            </div>
            <div className="lg:col-span-2">
              <Recomendaciones recos={recos} nuevas={recosNuevas} onDecidir={decidirReco} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}

// ── Estado de conexión / setup ────────────────────────────────────────────────
function ConexionCard({ ov, loading }) {
  const conectado = ov?.conectado
  if (loading && !ov) return null
  if (conectado) {
    return (
      <div className="card p-4 flex items-center gap-3 border-l-4 !border-l-emerald-500">
        <div className="w-9 h-9 rounded-xl bg-emerald-500/10 flex items-center justify-center">
          <Plug size={17} className="text-emerald-500" />
        </div>
        <div className="flex-1">
          <div className="text-[13.5px] font-semibold text-primary dark:text-slate-100">Meta Ads conectado</div>
          <div className="text-[11.5px] text-muted">
            {ov?.campanas_activas}/{ov?.campanas_total} campañas activas
            {ov?.ultima_sync && ` · última sync ${new Date(ov.ultima_sync).toLocaleString('es-AR')}`}
          </div>
        </div>
        {ov?.recomendaciones_nuevas > 0 && (
          <span className="chip-accent !text-[11px]">
            <Lightbulb size={11} /> {ov.recomendaciones_nuevas} recomendaciones
          </span>
        )}
      </div>
    )
  }
  return (
    <div className="card p-5 border-l-4 !border-l-amber-500">
      <div className="flex items-start gap-3">
        <div className="w-9 h-9 rounded-xl bg-amber-500/10 flex items-center justify-center shrink-0">
          <AlertTriangle size={17} className="text-amber-500" />
        </div>
        <div>
          <div className="text-[14px] font-semibold text-primary dark:text-slate-100 mb-1">
            Todavía no hay datos de Meta Ads
          </div>
          <p className="text-[12.5px] text-muted leading-relaxed max-w-xl">
            El agente analista (Claude Code + MCP de Meta Ads) sincroniza las campañas y métricas
            sobre el plan. Corré <code className="px-1 rounded bg-neutral-100 dark:bg-slate-800">meta-ads-analyst</code> en
            la carpeta <code className="px-1 rounded bg-neutral-100 dark:bg-slate-800">EQUIPO DE MARKETING</code> y
            empujará los datos acá automáticamente.
          </p>
        </div>
      </div>
    </div>
  )
}

// ── KPI card ──────────────────────────────────────────────────────────────────
function Kpi({ icon: Icon, label, value, sub, accent }) {
  return (
    <div className={`card p-4 ${accent ? 'bg-accent/5 dark:bg-accent/10' : ''}`}>
      <div className="flex items-center gap-2 mb-2 text-muted">
        <Icon size={14} className={accent ? 'text-accent' : ''} />
        <span className="text-[11.5px] font-medium tracking-tight">{label}</span>
      </div>
      <div className="text-[22px] font-semibold tracking-tight text-primary dark:text-slate-100 leading-none">
        {value}
      </div>
      {sub && <div className="text-[11px] text-muted mt-1.5">{sub}</div>}
    </div>
  )
}

// ── Mini bar chart de gasto (sin dependencias) ────────────────────────────────
function GastoChart({ serie }) {
  if (!serie.length) return null
  const max = Math.max(...serie.map(s => s.gasto), 1)
  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp size={15} className="text-accent" />
        <h3 className="text-[14px] font-semibold tracking-tight text-primary dark:text-slate-100">Gasto diario</h3>
      </div>
      <div className="flex items-end gap-1.5 h-36">
        {serie.map((s) => (
          <div key={s.fecha} className="flex-1 flex flex-col items-center justify-end group relative">
            <div className="w-full rounded-t-md bg-accent/70 hover:bg-accent transition-all"
                 style={{ height: `${(s.gasto / max) * 100}%`, minHeight: s.gasto ? '4px' : '0' }} />
            <div className="absolute -top-9 hidden group-hover:block bg-primary dark:bg-slate-700 text-neutral-50
                            text-[10.5px] rounded-lg px-2 py-1 whitespace-nowrap z-10 shadow-lg">
              {fmtMoneda(s.gasto)} · {fmtNum(s.conversiones)} conv.
            </div>
          </div>
        ))}
      </div>
      <div className="flex justify-between text-[10px] text-muted mt-2">
        <span>{serie[0]?.fecha?.slice(5)}</span>
        <span>{serie[serie.length - 1]?.fecha?.slice(5)}</span>
      </div>
    </div>
  )
}

// ── Tabla de campañas ─────────────────────────────────────────────────────────
function CampañasTabla({ camps }) {
  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 mb-4">
        <Megaphone size={15} className="text-accent" />
        <h3 className="text-[14px] font-semibold tracking-tight text-primary dark:text-slate-100">Campañas</h3>
      </div>
      {!camps.length ? (
        <div className="text-muted text-[12.5px] py-6 text-center">Sin campañas sincronizadas todavía.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-[12.5px]">
            <thead>
              <tr className="text-muted text-[11px] text-left border-b border-neutral-200/70 dark:border-slate-700/60">
                <th className="pb-2 font-medium">Campaña</th>
                <th className="pb-2 font-medium text-right">Gasto</th>
                <th className="pb-2 font-medium text-right">CTR</th>
                <th className="pb-2 font-medium text-right">CPC</th>
                <th className="pb-2 font-medium text-right">Conv.</th>
                <th className="pb-2 font-medium text-right">ROAS</th>
              </tr>
            </thead>
            <tbody>
              {camps.map(c => (
                <tr key={c.id} className="border-b border-neutral-100 dark:border-slate-800 last:border-0">
                  <td className="py-2.5 pr-2">
                    <div className="flex items-center gap-2">
                      <span className={`w-1.5 h-1.5 rounded-full ${c.estado === 'ACTIVE' ? 'bg-emerald-500' : 'bg-neutral-400'}`} />
                      <span className="font-medium text-primary dark:text-slate-100 truncate max-w-[180px]">{c.nombre}</span>
                    </div>
                    {c.objetivo && <div className="text-[10.5px] text-muted ml-3.5">{c.objetivo}</div>}
                  </td>
                  <td className="py-2.5 text-right text-primary dark:text-slate-200">{fmtMoneda(c.gasto_total, c.moneda)}</td>
                  <td className="py-2.5 text-right text-muted">{(c.ctr_prom || 0).toFixed(2)}%</td>
                  <td className="py-2.5 text-right text-muted">{fmtMoneda(c.cpc_prom, c.moneda)}</td>
                  <td className="py-2.5 text-right text-muted">{fmtNum(c.conversiones_total)}</td>
                  <td className="py-2.5 text-right font-medium text-primary dark:text-slate-200">
                    {c.roas_prom ? `${c.roas_prom.toFixed(2)}x` : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// ── Panel de recomendaciones ──────────────────────────────────────────────────
function Recomendaciones({ recos, nuevas, onDecidir }) {
  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles size={15} className="text-accent" />
        <h3 className="text-[14px] font-semibold tracking-tight text-primary dark:text-slate-100">
          Recomendaciones del agente
        </h3>
        {nuevas.length > 0 && <span className="chip-accent !text-[10.5px] ml-auto">{nuevas.length} nuevas</span>}
      </div>
      {!recos.length ? (
        <div className="text-muted text-[12.5px] py-6 text-center">
          El agente todavía no dejó recomendaciones.
        </div>
      ) : (
        <div className="space-y-3 max-h-[520px] overflow-y-auto pr-1">
          {recos.map(r => <RecoCard key={r.id} r={r} onDecidir={onDecidir} />)}
        </div>
      )}
    </div>
  )
}

function RecoCard({ r, onDecidir }) {
  const decidida = r.estado !== 'nueva'
  return (
    <div className={`rounded-2xl border p-3.5 transition-all ${
      decidida ? 'border-neutral-200/60 dark:border-slate-700/40 opacity-60'
               : 'border-neutral-200 dark:border-slate-700/60'}`}>
      <div className="flex items-center gap-2 mb-1.5 flex-wrap">
        <span className={`${SEV[r.severidad] || 'chip-muted'} !text-[10px]`}>{TIPO_LABEL[r.tipo] || r.tipo}</span>
        {r.campana_nombre && <span className="text-[10.5px] text-muted truncate max-w-[140px]">{r.campana_nombre}</span>}
        {r.estado === 'aplicada' && <span className="chip-success !text-[10px] ml-auto"><CheckCircle2 size={10} /> Aplicada</span>}
        {r.estado === 'descartada' && <span className="chip-danger !text-[10px] ml-auto"><XCircle size={10} /> Descartada</span>}
      </div>
      <div className="text-[13px] font-semibold text-primary dark:text-slate-100 leading-snug">{r.titulo}</div>
      {r.detalle && <p className="text-[11.5px] text-muted mt-1 leading-relaxed">{r.detalle}</p>}
      {r.accion_sugerida && (
        <div className="flex items-start gap-1.5 mt-2 text-[11.5px] text-accent">
          <ArrowUpRight size={13} className="mt-0.5 shrink-0" />
          <span>{r.accion_sugerida}</span>
        </div>
      )}
      {!decidida && (
        <div className="flex items-center gap-2 mt-2.5">
          <button onClick={() => onDecidir(r, 'aplicada')} className="btn-success !py-1 !px-2.5 !text-[11.5px]">
            <CheckCircle2 size={12} /> Aplicar
          </button>
          <button onClick={() => onDecidir(r, 'descartada')} className="btn-ghost !py-1 !px-2.5 !text-[11.5px]">
            <XCircle size={12} /> Descartar
          </button>
        </div>
      )}
    </div>
  )
}
