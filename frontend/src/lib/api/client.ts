export interface User {
  id: string
  email: string
  created_at: string | null
}

export class ApiError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.status = status
    this.detail = detail
  }
}

class ApiClient {
  private refreshPromise: Promise<boolean> | null = null

  onUnauth: (() => void) | null = null

  async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const res = await fetch(path, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include',
    })

    if (res.status === 401 && !path.includes('/auth/refresh')) {
      const refreshed = await this._tryRefresh()
      if (refreshed) {
        return this.request(method, path, body)
      }
      this.onUnauth?.()
    }

    if (!res.ok) {
      let detail = 'Request failed'
      try {
        const err = await res.json()
        detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail)
      } catch {}
      throw new ApiError(res.status, detail)
    }

    if (res.status === 204) return undefined as T

    return res.json()
  }

  private async _tryRefresh(): Promise<boolean> {
    if (!this.refreshPromise) {
      this.refreshPromise = (async () => {
        try {
          const res = await fetch('/api/auth/refresh', {
            method: 'POST',
            credentials: 'include',
          })
          return res.ok
        } catch {
          return false
        } finally {
          this.refreshPromise = null
        }
      })()
    }
    return this.refreshPromise
  }

  get<T>(path: string): Promise<T> {
    return this.request<T>('GET', path)
  }

  post<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('POST', path, body)
  }

  patch<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('PATCH', path, body)
  }

  put<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>('PUT', path, body)
  }

  del(path: string): Promise<void> {
    return this.request<void>('DELETE', path)
  }
}

export const api = new ApiClient()
