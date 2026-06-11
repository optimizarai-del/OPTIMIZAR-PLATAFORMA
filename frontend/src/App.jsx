import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import ProtectedRoute from './components/Layout/ProtectedRoute'
import Layout from './components/Layout/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ProyectoDetail from './pages/ProyectoDetail'
import Tareas from './pages/Tareas'
import Requerimientos from './pages/Requerimientos'
import NuevoRequerimiento from './pages/NuevoRequerimiento'
import CRM from './pages/CRM'
import Prospeccion from './pages/Prospeccion'
import Equipo from './pages/Equipo'
import Notificaciones from './pages/Notificaciones'

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login"    element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route path="/" element={
              <ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>
            } />
            <Route path="/proyecto/:id" element={
              <ProtectedRoute><Layout fullWidth><ProyectoDetail /></Layout></ProtectedRoute>
            } />
            <Route path="/tareas" element={
              <ProtectedRoute><Layout><Tareas /></Layout></ProtectedRoute>
            } />
            <Route path="/requerimientos" element={
              <ProtectedRoute><Layout><Requerimientos /></Layout></ProtectedRoute>
            } />
            <Route path="/requerimientos/nuevo" element={
              <ProtectedRoute><Layout><NuevoRequerimiento /></Layout></ProtectedRoute>
            } />
            <Route path="/crm" element={
              <ProtectedRoute><Layout fullWidth><CRM /></Layout></ProtectedRoute>
            } />
            <Route path="/prospeccion" element={
              <ProtectedRoute requireManager><Layout fullWidth><Prospeccion /></Layout></ProtectedRoute>
            } />
            <Route path="/equipo" element={
              <ProtectedRoute requireManager><Layout><Equipo /></Layout></ProtectedRoute>
            } />
            <Route path="/notificaciones" element={
              <ProtectedRoute requireManager><Layout><Notificaciones /></Layout></ProtectedRoute>
            } />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <Toaster
            position="bottom-right"
            gutter={8}
            toastOptions={{ duration: 3500 }}
          />
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}
