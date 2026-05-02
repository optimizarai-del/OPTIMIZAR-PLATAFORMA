// Hook simple para atajos de teclado globales.
// Uso:
//   useShortcut('Escape', onClose)
//   useShortcut('n', () => setOpen(true))
//   useShortcut(['cmd+k','ctrl+k'], openPalette)
import { useEffect } from 'react'

const isTypingTarget = (el) => {
  if (!el) return false
  const tag = el.tagName
  return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable
}

const matches = (e, combo) => {
  const parts = combo.toLowerCase().split('+')
  const key = parts[parts.length - 1]
  const wantCtrl = parts.includes('ctrl')
  const wantCmd = parts.includes('cmd') || parts.includes('meta')
  const wantShift = parts.includes('shift')
  const wantAlt = parts.includes('alt')

  const eventKey = e.key.toLowerCase()
  if (eventKey !== key) return false
  if (wantCtrl !== e.ctrlKey) return false
  if (wantCmd !== e.metaKey) return false
  if (wantShift !== e.shiftKey) return false
  if (wantAlt !== e.altKey) return false
  return true
}

export function useShortcut(combo, handler, opts = {}) {
  const { allowInInputs = false, enabled = true } = opts
  useEffect(() => {
    if (!enabled) return
    const combos = Array.isArray(combo) ? combo : [combo]
    const onKey = (e) => {
      if (!allowInInputs && isTypingTarget(document.activeElement)) {
        // Excepción: Escape siempre se permite para cerrar modales
        if (combos.every(c => c.toLowerCase() !== 'escape')) return
      }
      if (combos.some(c => matches(e, c))) {
        e.preventDefault()
        handler(e)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [combo, handler, allowInInputs, enabled])
}
