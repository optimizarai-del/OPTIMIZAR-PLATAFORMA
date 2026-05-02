// Skeleton loaders consistentes con el design system.
// Usar siempre que se esté esperando data de la red — mejor que un spinner solo o pantalla en blanco.

export function SkeletonBar({ className = '', w = 'w-full', h = 'h-3' }) {
  return <div className={`${w} ${h} rounded-md bg-neutral-200/70 dark:bg-slate-700/50 animate-pulse ${className}`} />
}

export function SkeletonCard({ className = '' }) {
  return (
    <div className={`card p-5 space-y-3 ${className}`}>
      <SkeletonBar w="w-2/3" h="h-4" />
      <SkeletonBar w="w-1/2" h="h-3" />
      <div className="pt-3 space-y-2">
        <SkeletonBar w="w-full" h="h-2" />
        <SkeletonBar w="w-5/6" h="h-2" />
      </div>
    </div>
  )
}

export function SkeletonRow({ className = '' }) {
  return (
    <div className={`card p-4 flex items-center gap-4 ${className}`}>
      <div className="w-8 h-8 rounded-lg bg-neutral-200/70 dark:bg-slate-700/50 animate-pulse" />
      <div className="flex-1 space-y-2">
        <SkeletonBar w="w-1/2" h="h-3" />
        <SkeletonBar w="w-1/3" h="h-2" />
      </div>
      <SkeletonBar w="w-16" h="h-3" />
    </div>
  )
}

export function SkeletonGrid({ count = 6, type = 'card' }) {
  const items = Array.from({ length: count })
  if (type === 'row') {
    return (
      <div className="space-y-3">
        {items.map((_, i) => <SkeletonRow key={i} />)}
      </div>
    )
  }
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {items.map((_, i) => <SkeletonCard key={i} />)}
    </div>
  )
}

export function SkeletonStats({ count = 4 }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="card p-5 space-y-2">
          <SkeletonBar w="w-20" h="h-2" />
          <SkeletonBar w="w-16" h="h-7" />
        </div>
      ))}
    </div>
  )
}
