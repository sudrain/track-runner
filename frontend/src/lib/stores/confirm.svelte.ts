interface ConfirmState {
  show: boolean
  message: string
  resolve: ((value: boolean) => void) | null
}

let _state = $state<ConfirmState>({
  show: false,
  message: '',
  resolve: null,
})

export function getConfirmState() {
  return _state
}

export function showConfirm(message: string): Promise<boolean> {
  return new Promise((resolve) => {
    _state = { show: true, message, resolve }
  })
}

export function confirmYes() {
  const resolve = _state.resolve
  _state = { show: false, message: '', resolve: null }
  resolve?.(true)
}

export function confirmNo() {
  const resolve = _state.resolve
  _state = { show: false, message: '', resolve: null }
  resolve?.(false)
}
