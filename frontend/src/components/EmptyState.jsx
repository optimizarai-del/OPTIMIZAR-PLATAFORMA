// EmptyState reusable: icono + título + descripción + (opcional) call-to-action.
// Mejor experiencia que "no hay datos" pelado.

export default function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  actionLabel,
  className = '',
}) {
  return (
    <div className={`card py-16 px-8 text-center flex flex-col items-center gap-4 animate-fade-in ${className}`}>
      {Icon && (
        <div className="w-14 h-14 rounded-2xl bg-accent/10 dark:bg-accent/15 flex items-center justify-center">
          <Icon size={24} className="text-accent" strokeWidth={1.5} />
        </div>
      )}
      <div className="space-y-1 max-w-md">
        <h3 className="font-semibold text-[15px] text-primary dark:text-slate-100 tracking-tight">{title}</h3>
        {description && (
          <p className="text-[13px] text-muted dark:text-slate-400 leading-relaxed">{description}</p>
        )}
      </div>
      {action && actionLabel && (
        <button onClick={action} className="btn-accent mt-1">
          {actionLabel}
        </button>
      )}
    </div>
  )
}
