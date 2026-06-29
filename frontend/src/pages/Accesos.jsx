import { useMemo, useState } from 'react'
import {
  Sparkles, MessageSquare, Clapperboard, Database, Github, Server,
  Workflow, BarChart3, NotebookText, Mail, Search, Send, MessageCircle,
  ExternalLink, Clock, Star
} from 'lucide-react'

/* ──────────────────────────────────────────────────────────────────────────
   Accesos directos a las IAs, infraestructura y herramientas que usa OPTIMIZAR.
   Para editar: cambiá la `url` de cada item (o agregá/quitá items abajo).
   `pronto: true` lo muestra como "Próximamente" (no abre, queda como recordatorio).
   ────────────────────────────────────────────────────────────────────────── */
const GRUPOS = [
  {
    titulo: 'IAs de generación',
    desc: 'Los cerebros con los que producimos contenido, código y video.',
    items: [
      { nombre: 'Claude', sub: 'Claude Code · plan Max', url: 'https://claude.ai', Icon: Sparkles, color: 'from-orange-500 to-amber-500' },
      { nombre: 'ChatGPT', sub: 'Texto + imágenes (OpenAI)', url: 'https://chat.openai.com', Icon: MessageSquare, color: 'from-emerald-500 to-teal-500' },
      { nombre: 'Higgsfield', sub: 'Video / reels con IA', url: 'https://higgsfield.ai', Icon: Clapperboard, color: 'from-fuchsia-500 to-purple-600' },
    ],
  },
  {
    titulo: 'Infraestructura y datos',
    desc: 'Dónde vive la plataforma, la base de datos y el código.',
    items: [
      { nombre: 'Supabase', sub: 'Base de datos · Auth', url: 'https://supabase.com/dashboard/project/cxronstvyedrtxuvwnjb', Icon: Database, color: 'from-green-500 to-emerald-600' },
      { nombre: 'EasyPanel', sub: 'Hosting · deploys', url: 'https://3buyoj.easypanel.host', Icon: Server, color: 'from-sky-500 to-blue-600' },
      { nombre: 'GitHub', sub: 'Repo de la plataforma', url: 'https://github.com/optimizarai-del/OPTIMIZAR-PLATAFORMA', Icon: Github, color: 'from-slate-600 to-slate-800' },
    ],
  },
  {
    titulo: 'Automatización y CRM',
    desc: 'Las herramientas que conectan y mueven los datos.',
    items: [
      { nombre: 'n8n', sub: 'Automatizaciones / workflows', url: 'https://n8n-nuevo-optimizar-front.3buyoj.easypanel.host', Icon: Workflow, color: 'from-rose-500 to-pink-600' },
      { nombre: 'Meta Ads', sub: 'Métricas (Pipeboard)', url: 'https://pipeboard.co', Icon: BarChart3, color: 'from-blue-500 to-indigo-600' },
      { nombre: 'Notion', sub: 'Documentación · tareas', url: 'https://notion.so', Icon: NotebookText, color: 'from-neutral-500 to-neutral-700' },
      { nombre: 'Google Workspace', sub: 'Gmail · Calendar · Drive', url: 'https://workspace.google.com', Icon: Mail, color: 'from-red-500 to-amber-500' },
    ],
  },
  {
    titulo: 'Outreach',
    desc: 'Prospección y envíos. Se activan cuando abramos las cuentas.',
    items: [
      { nombre: 'Apollo', sub: 'Base de prospectos', url: 'https://app.apollo.io', Icon: Search, color: 'from-violet-500 to-purple-600', pronto: true },
      { nombre: 'Instantly', sub: 'Email frío', url: 'https://app.instantly.ai', Icon: Send, color: 'from-cyan-500 to-sky-600', pronto: true },
      { nombre: 'WATI', sub: 'WhatsApp Business', url: 'https://app.wati.io', Icon: MessageCircle, color: 'from-green-500 to-lime-600', pronto: true },
    ],
  },
]

const FAVS_KEY = 'optimizar.accesos.favoritos'

function Card({ item, fav, onFav }) {
  const { nombre, sub, url, Icon, color, pronto } = item
  const Wrapper = pronto ? 'div' : 'a'
  const wrapperProps = pronto ? {} : { href: url, target: '_blank', rel: 'noreferrer' }

  return (
    <Wrapper
      {...wrapperProps}
      className={`group relative card p-5 flex items-center gap-4 transition-all duration-200
        ${pronto
          ? 'opacity-60 cursor-default'
          : 'hover:-translate-y-0.5 hover:shadow-lg focus-visible:ring-2 focus-visible:ring-accent outline-none'}`}
    >
      {/* Ícono en tile con gradiente de marca */}
      <div className={`shrink-0 w-12 h-12 rounded-2xl bg-gradient-to-br ${color}
                       flex items-center justify-center text-white shadow-soft`}>
        <Icon size={22} strokeWidth={2} />
      </div>

      <div className="min-w-0 flex-1">
        <div className="font-bold text-[15px] tracking-tight text-primary dark:text-slate-100 truncate">
          {nombre}
        </div>
        <div className="text-[12.5px] text-muted dark:text-slate-400 truncate">{sub}</div>
      </div>

      {/* Estrella de favorito (solo si abre) */}
      {!pronto && (
        <button
          type="button"
          onClick={(e) => { e.preventDefault(); onFav(nombre) }}
          aria-label={fav ? 'Quitar de favoritos' : 'Marcar favorito'}
          title={fav ? 'Quitar de favoritos' : 'Marcar favorito'}
          className="shrink-0 p-1.5 rounded-lg text-muted hover:text-warn transition-colors">
          <Star size={16} className={fav ? 'fill-warn text-warn' : ''} />
        </button>
      )}

      {/* Indicador de acción */}
      {pronto ? (
        <span className="shrink-0 inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wider
                         text-muted/70 bg-neutral-200/60 dark:bg-slate-700/60 rounded-full px-2 py-1">
          <Clock size={10} /> Pronto
        </span>
      ) : (
        <ExternalLink size={15} className="shrink-0 text-muted/40 group-hover:text-accent transition-colors" />
      )}
    </Wrapper>
  )
}

export default function Accesos() {
  const [favs, setFavs] = useState(() => {
    try { return JSON.parse(localStorage.getItem(FAVS_KEY) || '[]') } catch { return [] }
  })

  const toggleFav = (nombre) => {
    setFavs(prev => {
      const next = prev.includes(nombre) ? prev.filter(n => n !== nombre) : [...prev, nombre]
      localStorage.setItem(FAVS_KEY, JSON.stringify(next))
      return next
    })
  }

  const favoritos = useMemo(() => {
    if (!favs.length) return []
    const all = GRUPOS.flatMap(g => g.items)
    return favs.map(n => all.find(i => i.nombre === n)).filter(Boolean)
  }, [favs])

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <header className="mb-10">
        <div className="hero-eyebrow">Herramientas</div>
        <h1 className="hero-title text-5xl md:text-6xl mb-3">Accesos directos.</h1>
        <p className="hero-sub">Todas las IAs, cuentas y herramientas que usamos, a un clic. Se abren en una pestaña nueva.</p>
      </header>

      {/* Favoritos */}
      {favoritos.length > 0 && (
        <section className="mb-10">
          <div className="section-label !mt-0 flex items-center gap-1.5 mb-3">
            <Star size={10} className="text-warn fill-warn" /> Favoritos
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {favoritos.map(item => (
              <Card key={`fav-${item.nombre}`} item={item} fav onFav={toggleFav} />
            ))}
          </div>
        </section>
      )}

      {/* Grupos */}
      <div className="space-y-10">
        {GRUPOS.map(grupo => (
          <section key={grupo.titulo}>
            <div className="mb-3">
              <h2 className="font-bold text-lg tracking-tight text-primary dark:text-slate-100">{grupo.titulo}</h2>
              <p className="text-[13px] text-muted dark:text-slate-400">{grupo.desc}</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {grupo.items.map(item => (
                <Card
                  key={item.nombre}
                  item={item}
                  fav={favs.includes(item.nombre)}
                  onFav={toggleFav}
                />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
