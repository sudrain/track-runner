export interface Toast {
  id: number
  message: string
  type: 'success' | 'error'
}

let _toasts = $state<Toast[]>([])

export function getToasts() {
  return _toasts
}

export function showToast(message: string, type: 'success' | 'error' = 'success') {
  const id = Date.now() + Math.random()
  _toasts = [..._toasts, { id, message, type }]
  setTimeout(() => {
    _toasts = _toasts.filter(t => t.id !== id)
  }, 3500)
}

export function dismissToast(id: number) {
  _toasts = _toasts.filter(t => t.id !== id)
}
