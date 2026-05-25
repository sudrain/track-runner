import { api, ApiError } from '../api/client'

export interface ExerciseTemplateOut {
  id: number
  name: string
}

export interface CardioIntervalOut {
  id: number
  duration_minutes: number
  distance_km: number
  tempo_min_per_km: number | null
  avg_heart_rate: number | null
}

export interface CardioWorkoutOut {
  id: number
  name: string
  datetime: string
  notes: string
  intervals: CardioIntervalOut[]
}

export interface CardioIntervalCreate {
  duration_minutes: number
  distance_km: number
  tempo_min_per_km?: number | null
  avg_heart_rate?: number | null
}

export interface CardioWorkoutCreate {
  name: string
  datetime: string
  notes: string
  intervals: CardioIntervalCreate[]
}

export interface CardioWorkoutUpdate {
  name?: string
  datetime?: string
  notes?: string
  intervals?: CardioIntervalCreate[]
}

interface PaginatedResponse<T> {
  items: T[]
  total: number
}

class CardioStore {
  list = $state<CardioWorkoutOut[]>([])
  total = $state(0)
  loading = $state(false)
  error = $state<string | null>(null)
  current = $state<CardioWorkoutOut | null>(null)
  currentLoading = $state(false)
  templates = $state<ExerciseTemplateOut[]>([])
  templatesLoading = $state(false)

  async fetchTemplates() {
    this.templatesLoading = true
    try {
      this.templates = await api.get<ExerciseTemplateOut[]>('/api/exercise-templates?type=cardio')
    } catch {
      this.templates = []
    } finally {
      this.templatesLoading = false
    }
  }

  async fetchList(offset = 0, limit = 200) {
    this.loading = true
    this.error = null
    try {
      const res = await api.get<PaginatedResponse<CardioWorkoutOut>>(
        `/api/cardio?offset=${offset}&limit=${limit}`
      )
      this.list = res.items
      this.total = res.total
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Failed to load workouts'
    } finally {
      this.loading = false
    }
  }

  async fetchOne(id: number) {
    this.currentLoading = true
    this.error = null
    try {
      this.current = await api.get<CardioWorkoutOut>(`/api/cardio/${id}`)
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Failed to load workout'
    } finally {
      this.currentLoading = false
    }
  }

  async create(data: CardioWorkoutCreate) {
    this.error = null
    return api.post<CardioWorkoutOut>('/api/cardio', data)
  }

  async update(id: number, data: CardioWorkoutUpdate) {
    this.error = null
    this.current = await api.put<CardioWorkoutOut>(`/api/cardio/${id}`, data)
    return this.current
  }

  async remove(id: number) {
    this.error = null
    await api.del(`/api/cardio/${id}`)
  }
}

export const cardio = new CardioStore()

// ---------- Strength ----------

export interface SetOut {
  id: number
  weight_kg: number
  repetitions: number
}

export interface ExerciseOut {
  id: number
  name: string
  sets: SetOut[]
}

export interface StrengthWorkoutOut {
  id: number
  datetime: string
  notes: string
  exercises: ExerciseOut[]
}

export interface SetCreate {
  weight_kg: number
  repetitions: number
}

export interface ExerciseCreate {
  name: string
  sets: SetCreate[]
}

export interface StrengthWorkoutCreate {
  datetime: string
  notes: string
  exercises: ExerciseCreate[]
}

export interface StrengthWorkoutUpdate {
  datetime?: string
  notes?: string
  exercises?: ExerciseCreate[]
}

class StrengthStore {
  list = $state<StrengthWorkoutOut[]>([])
  total = $state(0)
  loading = $state(false)
  error = $state<string | null>(null)
  current = $state<StrengthWorkoutOut | null>(null)
  currentLoading = $state(false)
  templates = $state<ExerciseTemplateOut[]>([])
  templatesLoading = $state(false)

  async fetchTemplates(type?: string) {
    this.templatesLoading = true
    try {
      const url = type ? `/api/exercise-templates?type=${type}` : '/api/exercise-templates'
      this.templates = await api.get<ExerciseTemplateOut[]>(url)
    } catch {
      this.templates = []
    } finally {
      this.templatesLoading = false
    }
  }

  async fetchList(offset = 0, limit = 200) {
    this.loading = true
    this.error = null
    try {
      const res = await api.get<PaginatedResponse<StrengthWorkoutOut>>(
        `/api/strength?offset=${offset}&limit=${limit}`
      )
      this.list = res.items
      this.total = res.total
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Failed to load workouts'
    } finally {
      this.loading = false
    }
  }

  async fetchOne(id: number) {
    this.currentLoading = true
    this.error = null
    try {
      this.current = await api.get<StrengthWorkoutOut>(`/api/strength/${id}`)
    } catch (e) {
      this.error = e instanceof ApiError ? e.detail : 'Failed to load workout'
    } finally {
      this.currentLoading = false
    }
  }

  async create(data: StrengthWorkoutCreate) {
    this.error = null
    return api.post<StrengthWorkoutOut>('/api/strength', data)
  }

  async update(id: number, data: StrengthWorkoutUpdate) {
    this.error = null
    this.current = await api.put<StrengthWorkoutOut>(`/api/strength/${id}`, data)
    return this.current
  }

  async remove(id: number) {
    this.error = null
    await api.del(`/api/strength/${id}`)
  }
}

export const strength = new StrengthStore()
