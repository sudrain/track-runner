<script lang="ts">
  import { auth } from '../lib/stores/auth.svelte'
  import { stats } from '../lib/stores/stats.svelte'
  import { navigate } from '../lib/router.svelte'
  import { api } from '../lib/api/client'
  import { formatDateShort } from '../lib/utils/format'
  import { formatTempoShort } from '../lib/utils/tempo'
  import Skeleton from '../lib/components/Skeleton.svelte'
  import type { CardioWorkoutOut, CardioIntervalOut, StrengthWorkoutOut } from '../lib/stores/workouts.svelte'

  let recentCardio = $state<CardioWorkoutOut[]>([])
  let recentStrength = $state<StrengthWorkoutOut[]>([])
  let recentLoading = $state(true)

  async function fetchRecent() {
    recentLoading = true
    try {
      const [cardioRes, strengthRes] = await Promise.all([
        api.get<{ items: CardioWorkoutOut[]; total: number }>('/api/cardio?offset=0&limit=5'),
        api.get<{ items: StrengthWorkoutOut[]; total: number }>('/api/strength?offset=0&limit=5'),
      ])
      recentCardio = cardioRes.items
      recentStrength = strengthRes.items
    } catch {
    } finally {
      recentLoading = false
    }
  }

  $effect(() => {
    if (auth.user) {
      stats.fetch()
      fetchRecent()
    } else {
      stats.data = null
      recentCardio = []
      recentStrength = []
    }
  })

  function totalKm(intervals: CardioIntervalOut[]): number {
    return intervals.reduce((s, i) => s + i.distance_km, 0)
  }

  function workoutTempo(intervals: CardioIntervalOut[]): number | null {
    const t = intervals.reduce((s, i) => s + i.duration_minutes, 0)
    const d = intervals.reduce((s, i) => s + i.distance_km, 0)
    return d > 0 ? t / d : null
  }

  function totalVolume(exercises: { sets: { weight_kg: number; repetitions: number }[] }[]): number {
    return exercises.reduce((s, ex) => s + ex.sets.reduce((ss, set) => ss + set.weight_kg * set.repetitions, 0), 0)
  }
</script>

{#if auth.user}
  <div>
    {#if stats.loading}
      <div class="grid grid-cols-3 gap-2 sm:gap-4 mb-8">
        {#each [1, 2, 3] as _}
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-3 sm:p-4 space-y-2">
            <Skeleton class="h-3 w-12" />
            <Skeleton class="h-7 w-20" />
            <Skeleton class="h-3 w-16" />
          </div>
        {/each}
      </div>
    {:else if stats.error}
      <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3 mb-4">{stats.error}</div>
    {:else if stats.data}
      <div class="grid grid-cols-3 gap-2 sm:gap-4 mb-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-3 sm:p-4">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Неделя</p>
          <p class="text-xl sm:text-2xl font-bold text-indigo-600">{stats.data.week_km.toFixed(1)} km</p>
          <p class="text-xs text-gray-400 mt-1">{formatTempoShort(stats.data.week_avg_tempo)} /km</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-3 sm:p-4">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Месяц</p>
          <p class="text-xl sm:text-2xl font-bold text-indigo-600">{stats.data.month_km.toFixed(1)} km</p>
          <p class="text-xs text-gray-400 mt-1">{formatTempoShort(stats.data.month_avg_tempo)} /km</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-3 sm:p-4">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Год</p>
          <p class="text-xl sm:text-2xl font-bold text-indigo-600">{stats.data.year_km.toFixed(1)} km</p>
          <p class="text-xs text-gray-400 mt-1">{formatTempoShort(stats.data.year_avg_tempo)} /km</p>
        </div>
      </div>
    {/if}

    <div class="flex gap-3 mb-8">
      <button
        onclick={() => navigate('cardio-new')}
        class="flex-1 bg-indigo-600 text-white rounded-xl px-8 py-6 sm:px-6 sm:py-4 text-xl sm:text-lg font-bold hover:bg-indigo-700 active:bg-indigo-800 shadow-md"
      >
        Кардио
      </button>
      <button
        onclick={() => navigate('strength-new')}
        class="flex-1 bg-indigo-600 text-white rounded-xl px-8 py-6 sm:px-6 sm:py-4 text-xl sm:text-lg font-bold hover:bg-indigo-700 active:bg-indigo-800 shadow-md"
      >
        Силовая
      </button>
    </div>

    {#if recentLoading}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-5 space-y-3">
          <Skeleton class="h-5 w-32" />
          {#each [1, 2, 3] as _}
            <Skeleton class="h-12 w-full rounded-lg" />
          {/each}
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-5 space-y-3">
          <Skeleton class="h-5 w-36" />
          {#each [1, 2, 3] as _}
            <Skeleton class="h-12 w-full rounded-lg" />
          {/each}
        </div>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-5">
          <h2 class="text-base font-semibold text-gray-700 mb-3">Последние кардио</h2>
          {#if recentCardio.length === 0}
            <p class="text-gray-400 text-base">Пока нет кардио-тренировок</p>
          {:else}
            <div class="space-y-2">
              {#each recentCardio as w}
                <button
                  onclick={() => navigate('cardio-detail', { id: w.id })}
                  class="w-full text-left flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50 text-base"
                >
                  <div>
                    <span class="font-medium text-gray-800">{w.name}</span>
                    <span class="text-gray-400 ml-2">{formatDateShort(w.datetime)}</span>
                  </div>
                  <span class="text-gray-500">
                    {totalKm(w.intervals).toFixed(2)} км · {formatTempoShort(workoutTempo(w.intervals))}
                  </span>
                </button>
              {/each}
            </div>
          {/if}
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 class="text-base font-semibold text-gray-700 mb-3">Последние силовые</h2>
          {#if recentStrength.length === 0}
            <p class="text-gray-400 text-base">Пока нет силовых тренировок</p>
          {:else}
            <div class="space-y-2">
              {#each recentStrength as w}
                <button
                  onclick={() => navigate('strength-detail', { id: w.id })}
                  class="w-full text-left flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50 text-base"
                >
                  <div>
                    <span class="font-medium text-gray-800">{w.exercises.length} exercises</span>
                    <span class="text-gray-400 ml-2">{formatDateShort(w.datetime)}</span>
                  </div>
                  <span class="text-gray-500">
                    {totalVolume(w.exercises).toFixed(0)} кг
                  </span>
                </button>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
{:else}
  <div class="text-center py-16">
    <h1 class="text-4xl font-bold text-gray-800 mb-4">Track Runner</h1>
    <p class="text-gray-500 text-lg mb-8">Ваш дневник тренировок</p>
    <div class="flex gap-4 justify-center">
      <a
        href="#/login"
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
      >
        Войти
      </a>
      <a
        href="#/register"
        class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
      >
        Регистрация
      </a>
    </div>
  </div>
{/if}
