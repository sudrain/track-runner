import { describe, it, expect, beforeEach } from 'vitest'
import { showConfirm, confirmYes, confirmNo, getConfirmState } from '../confirm.svelte'

describe('confirm store', () => {
  beforeEach(() => {
    if (getConfirmState().show) {
      confirmNo()
    }
  })

  it('should show confirm dialog with message', async () => {
    const promise = showConfirm('Delete this?')
    expect(getConfirmState().show).toBe(true)
    expect(getConfirmState().message).toBe('Delete this?')
    confirmYes()
    expect(await promise).toBe(true)
  })

  it('should return false on cancel', async () => {
    const promise = showConfirm('Cancel?')
    confirmNo()
    expect(await promise).toBe(false)
  })

  it('should hide dialog after confirm', () => {
    showConfirm('test')
    confirmYes()
    expect(getConfirmState().show).toBe(false)
  })

  it('should hide dialog after cancel', () => {
    showConfirm('test')
    confirmNo()
    expect(getConfirmState().show).toBe(false)
  })
})
