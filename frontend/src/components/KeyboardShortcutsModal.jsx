import { Keyboard, X } from 'lucide-react'
import { useShortcut } from '../utils/useShortcut'

const SECCIONES = [
  {
    title: 'Navegación',
    items: [
      { keys: ['?'], desc: 'Mostrar esta ayuda' },
      { keys: ['Esc'], desc: 'Cerrar modal o drawer' },
    ],
  },
  {
    title: 'Dashboard de proyectos',
    items: [
      { keys: ['N'], desc: 'Nuevo proyecto (manager+)' },
    ],
  },
  {
    title: 'Detalle del proyecto',
    items: [
      { keys: ['T'], desc: 'Nueva tarea' },
      { keys: ['P'], desc: 'Nuevo punto del plan' },
    ],
  },
]

function Kbd({ children }) {
  return (
    <kbd className="px-2 py-1 text-[11px] font-mono rounded-md
                    bg-neutral-100 dark:bg-slate-700/60
                    border border-border/60 dark:border-slate-600/60
                    text-primary dark:text-slate-200 font-semibold shadow-sm">
      {children}
    </kbd>
  )
}

export default function KeyboardShortcutsModal({ onClose }) {
  useShortcut('Escape', onClose)
  return (
    <div className="fixed inset-0 bg-primary/30 backdrop-blur-sm z-[60] grid place-items-center p-6"
      onClick={onClose}>
      <div className="card p-7 max-w-md w-full shadow-lift animate-scale-in"
        onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Keyboard size={16} className="text-accent" />
            <h2 className="font-semibold text-[15px] tracking-tight">Atajos de teclado</h2>
          </div>
          <button onClick={onClose}
            className="text-muted hover:text-primary transition p-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-slate-700">
            <X size={16} />
          </button>
        </div>
        <div className="space-y-5">
          {SECCIONES.map(s => (
            <div key={s.title}>
              <div className="text-[11px] uppercase tracking-wider text-muted font-semibold mb-2">
                {s.title}
              </div>
              <div className="space-y-1.5">
                {s.items.map((item, i) => (
                  <div key={i} className="flex items-center justify-between py-1.5">
                    <span className="text-[13px] text-primary dark:text-slate-200">{item.desc}</span>
                    <div className="flex gap-1">
                      {item.keys.map((k, j) => <Kbd key={j}>{k}</Kbd>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <p className="mt-6 text-[11px] text-muted text-center">
          Tip: cuando estás en un input los atajos se ignoran (excepto <Kbd>Esc</Kbd>).
        </p>
      </div>
    </div>
  )
}
