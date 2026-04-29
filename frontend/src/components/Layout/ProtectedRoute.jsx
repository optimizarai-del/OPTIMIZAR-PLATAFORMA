import { Navigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function ProtectedRoute({ children, requireManager }) {
  const { user, loading, isManager } = useAuth()
  if (loading) return (
    <div className="min-h-screen bg-bg grid place-items-center">
      <div className="w-6 h-6 rounded-full border-2 border-accent border-t-transparent animate-spin" />
    </div>
  )
  if (!user) return <Navigate to="/login" replace />
  if (requireManager && !isManager) return <Navigate to="/" replace />
  return children
}
