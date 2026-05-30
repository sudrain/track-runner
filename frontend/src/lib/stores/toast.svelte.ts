export interface Toast {
  id: string
  message: string
  type: 'success' | 'error'
}

let _toasts = $state<Toast[]>([])

export function getToasts() {
  return _toasts
}

export function showToast(message: string, type: 'success' | 'error' = 'success') {
  const id = crypto.randomUUID()
  _toasts = [..._toasts, { id, message, type }]
  setTimeout(() => {
    _toasts = _toasts.filter(t => t.id !== id)
  }, 3500)
}

export function dismissToast(id: string) {
  _toasts = _toasts.filter(t => t.id !== id)
}
