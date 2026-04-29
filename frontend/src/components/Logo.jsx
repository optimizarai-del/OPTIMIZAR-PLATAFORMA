export default function Logo({ size = 'md', tagline = false, color = 'primary', className = '' }) {
  const sizes = {
    xs: { txt: 'text-lg',  dot: 'w-1.5 h-1.5 ml-0.5', tag: 'text-[8px]' },
    sm: { txt: 'text-xl',  dot: 'w-2 h-2 ml-0.5',     tag: 'text-[9px]' },
    md: { txt: 'text-2xl', dot: 'w-2.5 h-2.5 ml-0.5', tag: 'text-[10px]' },
    lg: { txt: 'text-5xl', dot: 'w-4 h-4 ml-1',       tag: 'text-xs' },
    xl: { txt: 'text-7xl', dot: 'w-6 h-6 ml-1.5',     tag: 'text-sm' },
  }
  const s = sizes[size] || sizes.md
  const colors = {
    primary: 'text-primary',
    neutral: 'text-neutral-50',
    white:   'text-white',
  }

  return (
    <div className={`inline-flex flex-col leading-none ${className}`}>
      <div className={`flex items-end font-display font-bold tracking-[-0.04em] ${colors[color]} ${s.txt}`}>
        <span>Optimizar</span>
        <span className={`${s.dot} bg-accent rounded-[2px] mb-[0.15em] ml-1`} aria-hidden />
      </div>
      {tagline && (
        <div className={`${s.tag} font-medium tracking-[0.18em] uppercase mt-1.5 ${
          color === 'primary' ? 'text-accent-600' : 'text-accent-300'
        }`}>
          Automatización · Eficiencia · Resultados
        </div>
      )}
    </div>
  )
}
