import { api, ApiError } from '../api/client'

export interface RunningStats {
  week_km: number
  month_km: number
  year_km: number
  week_avg_tempo: number | null
  month_avg_tempo: number | null
  year_avg_tempo: number | null
}

class StatsStore {
  data = $state<RunningStats | null>(null)
  loading = $state(true)
  error = $state<string | null>(null)

  async fetch() {
    this.loading = true
    this.error = null
    try {
      this.data = await api.get<RunningStats>('/api/statistics/running')
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        this.data = null
      } else {
        this.error = e instanceof ApiError ? e.detail : 'Failed to load statistics'
      }
    } finally {
      this.loading = false
    }
  }
}

export const stats = new StatsStore()
