import { describe, it, expect, vi, beforeEach } from 'vitest'
import { showToast, dismissToast, getToasts } from '../toast.svelte'

describe('toast store', () => {
  beforeEach(() => {
    while (getToasts().length) {
      dismissToast(getToasts()[0].id)
    }
  })

  it('should add a success toast', () => {
    showToast('hello', 'success')
    expect(getToasts()).toHaveLength(1)
    expect(getToasts()[0].message).toBe('hello')
    expect(getToasts()[0].type).toBe('success')
  })

  it('should add an error toast', () => {
    showToast('error!', 'error')
    expect(getToasts()).toHaveLength(1)
    expect(getToasts()[0].type).toBe('error')
  })

  it('should dismiss a toast by id', () => {
    showToast('test')
    const id = getToasts()[0].id
    dismissToast(id)
    expect(getToasts()).toHaveLength(0)
  })

  it('should auto-dismiss after timeout', async () => {
    vi.useFakeTimers()
    showToast('auto dismiss')
    expect(getToasts()).toHaveLength(1)
    vi.advanceTimersByTime(3600)
    expect(getToasts()).toHaveLength(0)
    vi.useRealTimers()
  })

  it('should allow multiple toasts simultaneously', () => {
    showToast('first')
    showToast('second')
    showToast('third')
    expect(getToasts()).toHaveLength(3)
  })
})
