import HUD from '../HUD'
import Sidebar from './Sidebar'

export default function Layout({ children, fullWidth = false }) {
  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-slate-900 transition-colors duration-200">
      <HUD />
      <div className="flex">
        <Sidebar />
        <main className={`flex-1 ${fullWidth ? '' : 'px-10 py-12'} overflow-x-hidden`}>
          {children}
        </main>
      </div>
    </div>
  )
}
