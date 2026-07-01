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
import Servicios from './pages/Servicios'
import CRM from './pages/CRM'
import Contactos from './pages/Contactos'
import Prospeccion from './pages/Prospeccion'
import Marketing from './pages/Marketing'
import Agentes from './pages/Agentes'
import Equipo from './pages/Equipo'
import Notificaciones from './pages/Notificaciones'
import Accesos from './pages/Accesos'

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
            <Route path="/servicios" element={
              <ProtectedRoute><Layout fullWidth><Servicios /></Layout></ProtectedRoute>
            } />
            <Route path="/crm" element={
              <ProtectedRoute><Layout fullWidth><CRM /></Layout></ProtectedRoute>
            } />
            <Route path="/contactos" element={
              <ProtectedRoute><Layout><Contactos /></Layout></ProtectedRoute>
            } />
            <Route path="/prospeccion" element={
              <ProtectedRoute requireManager><Layout fullWidth><Prospeccion /></Layout></ProtectedRoute>
            } />
            <Route path="/marketing" element={
              <ProtectedRoute requireManager><Layout fullWidth><Marketing /></Layout></ProtectedRoute>
            } />
            <Route path="/agentes" element={
              <ProtectedRoute requireManager><Layout fullWidth><Agentes /></Layout></ProtectedRoute>
            } />
            <Route path="/equipo" element={
              <ProtectedRoute requireManager><Layout><Equipo /></Layout></ProtectedRoute>
            } />
            <Route path="/notificaciones" element={
              <ProtectedRoute requireManager><Layout><Notificaciones /></Layout></ProtectedRoute>
            } />
            <Route path="/accesos" element={
              <ProtectedRoute><Layout><Accesos /></Layout></ProtectedRoute>
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
