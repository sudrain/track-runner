import { api, ApiError, type User } from '../api/client'
import { navigate } from '../router'

class AuthStore {
  user = $state<User | null>(null)
  loading = $state(true)
  error = $state<string | null>(null)

  async checkAuth() {
    this.loading = true
    this.error = null
    try {
      this.user = await api.get<User>('/api/auth/me')
    } catch {
      this.user = null
    } finally {
      this.loading = false
    }
  }

  async login(email: string, password: string) {
    this.loading = true
    this.error = null
    try {
      this.user = await api.post<User>('/api/auth/login', { email, password })
      navigate('home')
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Login failed'
      throw e
    } finally {
      this.loading = false
    }
  }

  async register(email: string, password: string) {
    this.loading = true
    this.error = null
    try {
      this.user = await api.post<User>('/api/auth/register', { email, password })
      navigate('home')
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Registration failed'
      throw e
    } finally {
      this.loading = false
    }
  }

  async logout() {
    try {
      await api.post('/api/auth/logout')
    } catch {
    } finally {
      this.user = null
      navigate('home')
    }
  }
}

export const auth = new AuthStore()

api.onUnauth = () => {
  auth.user = null
}
