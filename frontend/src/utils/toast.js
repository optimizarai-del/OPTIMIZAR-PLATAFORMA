// Wrapper sobre react-hot-toast que respeta el design system de Optimizar.
// Usar: import { toast } from '@/utils/toast'  → toast.success('...'), toast.error('...'), toast.promise(...)
import toastLib from 'react-hot-toast'

const baseStyle = {
  borderRadius: '12px',
  padding: '12px 16px',
  fontSize: '13px',
  fontWeight: 500,
  letterSpacing: '-0.01em',
  boxShadow: '0 8px 24px rgba(15, 23, 42, 0.12)',
}

export const toast = {
  success: (msg) => toastLib.success(msg, {
    duration: 3500,
    style: { ...baseStyle, background: '#059669', color: '#fff' },
    iconTheme: { primary: '#fff', secondary: '#059669' },
  }),

  error: (msg) => toastLib.error(msg, {
    duration: 5000,
    style: { ...baseStyle, background: '#DC2626', color: '#fff' },
    iconTheme: { primary: '#fff', secondary: '#DC2626' },
  }),

  loading: (msg) => toastLib.loading(msg, {
    style: { ...baseStyle, background: '#1E293B', color: '#fff' },
  }),

  info: (msg) => toastLib(msg, {
    duration: 3000,
    style: { ...baseStyle, background: '#1E293B', color: '#fff' },
    icon: 'ℹ️',
  }),

  // promise(p, { loading, success, error })
  promise: (promise, msgs) => toastLib.promise(promise, msgs, {
    style: baseStyle,
    success: { style: { ...baseStyle, background: '#059669', color: '#fff' } },
    error: { style: { ...baseStyle, background: '#DC2626', color: '#fff' } },
    loading: { style: { ...baseStyle, background: '#1E293B', color: '#fff' } },
  }),

  dismiss: toastLib.dismiss,
}

export default toast
