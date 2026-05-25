<script lang="ts">
  import { cardio, type CardioIntervalOut, type CardioWorkoutOut } from '../lib/stores/workouts.svelte'
  import { navigate } from '../lib/router'
  import Pagination from '../lib/components/Pagination.svelte'
  import { formatDateShort } from '../lib/utils/format'
  import { formatTempoShort } from '../lib/utils/tempo'
  import { showConfirm } from '../lib/stores/confirm.svelte'
  import { showToast } from '../lib/stores/toast.svelte'

  let offset = $state(0)
  let limit = $state(20)
  type SortCol = 'name' | 'date' | 'distance' | 'duration' | 'tempo' | 'hr'
  let sortCol = $state<SortCol>('date')
  let sortDir = $state<'asc' | 'desc'>('desc')

  $effect(() => {
    cardio.fetchList(offset, limit)
  })

  function toggleSort(col: SortCol) {
    if (sortCol === col) {
      sortDir = sortDir === 'asc' ? 'desc' : 'asc'
    } else {
      sortCol = col
      sortDir = 'desc'
    }
  }

  function sortKey(w: CardioWorkoutOut): number | string {
    switch (sortCol) {
      case 'name': return w.name
      case 'date': return w.datetime
      case 'distance': return totalKm(w.intervals)
      case 'duration': return totalMin(w.intervals)
      case 'tempo': return workoutTempo(w.intervals) ?? Infinity
      case 'hr': return avgHr(w.intervals) ?? -Infinity
    }
  }

  let sorted = $derived(
    [...cardio.list].sort((a, b) => {
      const ka = sortKey(a)
      const kb = sortKey(b)
      if (ka < kb) return sortDir === 'asc' ? -1 : 1
      if (ka > kb) return sortDir === 'asc' ? 1 : -1
      return 0
    })
  )

  function sortIcon(col: SortCol): string {
    if (sortCol !== col) return ''
    return sortDir === 'asc' ? ' ▲' : ' ▼'
  }

  function handleLimitChange(newLimit: number) {
    limit = newLimit
    offset = 0
  }

  function exportCsv() {
    const rows = cardio.list.map(w => {
      const km = totalKm(w.intervals)
      const min = totalMin(w.intervals)
      return `${w.name},${formatDateShort(w.datetime)},${km.toFixed(2)},${min.toFixed(0)},${formatTempoShort(workoutTempo(w.intervals))},${avgHr(w.intervals) ?? ''}`
    })
    const csv = 'Name,Date,Km,Min,Tempo,HR\n' + rows.join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'cardio-workouts.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  function goToDetail(id: number) {
    navigate('cardio-detail', { id })
  }

  async function deleteWorkout(id: number) {
    const ok = await showConfirm('Delete this workout?')
    if (!ok) return
    try {
      await cardio.remove(id)
      showToast('Workout deleted')
      cardio.fetchList(offset, limit)
    } catch {
      showToast('Failed to delete workout', 'error')
    }
  }

  function workoutTempo(intervals: CardioIntervalOut[]): number | null {
    const totalMin = intervals.reduce((s, i) => s + i.duration_minutes, 0)
    const totalKm = intervals.reduce((s, i) => s + i.distance_km, 0)
    if (totalKm <= 0) return null
    return totalMin / totalKm
  }

  function avgHr(intervals: CardioIntervalOut[]): number | null {
    const withHr = intervals.filter(i => i.avg_heart_rate !== null)
    if (withHr.length === 0) return null
    return Math.round(withHr.reduce((s, i) => s + i.avg_heart_rate!, 0) / withHr.length)
  }

  function totalKm(intervals: CardioIntervalOut[]): number {
    return intervals.reduce((s, i) => s + i.distance_km, 0)
  }

  function totalMin(intervals: CardioIntervalOut[]): number {
    return intervals.reduce((s, i) => s + i.duration_minutes, 0)
  }
</script>

<div>
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Cardio Workouts</h1>
    <button
      onclick={() => navigate('cardio-new')}
      class="bg-indigo-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-indigo-700"
    >
      + New Workout
    </button>
  </div>

  {#if cardio.loading}
    <div class="text-gray-400 text-center py-12">Loading...</div>
  {:else if cardio.error}
    <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3">{cardio.error}</div>
  {:else if cardio.list.length === 0}
    <div class="text-gray-400 text-center py-12">No workouts yet. Create your first one!</div>
  {:else}
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-200 text-left text-gray-500">
            <th onclick={() => toggleSort('name')} class="pb-3 font-medium cursor-pointer hover:text-gray-700 select-none">Name{sortIcon('name')}</th>
            <th onclick={() => toggleSort('date')} class="pb-3 font-medium cursor-pointer hover:text-gray-700 select-none">Date{sortIcon('date')}</th>
            <th onclick={() => toggleSort('distance')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">Km{sortIcon('distance')}</th>
            <th onclick={() => toggleSort('duration')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">Min{sortIcon('duration')}</th>
            <th onclick={() => toggleSort('tempo')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">Tempo{sortIcon('tempo')}</th>
            <th onclick={() => toggleSort('hr')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">HR{sortIcon('hr')}</th>
            <th class="pb-3 font-medium text-right"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          {#each sorted as workout}
            <tr class="hover:bg-gray-50 cursor-pointer" onclick={() => goToDetail(workout.id)}>
              <td class="py-3 font-medium text-gray-800">{workout.name}</td>
              <td class="py-3 text-gray-500">{formatDateShort(workout.datetime)}</td>
              <td class="py-3 text-right text-gray-700">{totalKm(workout.intervals).toFixed(2)}</td>
              <td class="py-3 text-right text-gray-700">{totalMin(workout.intervals).toFixed(0)}</td>
              <td class="py-3 text-right text-gray-700">{formatTempoShort(workoutTempo(workout.intervals))}</td>
              <td class="py-3 text-right text-gray-700">{avgHr(workout.intervals) ?? '—'}</td>
              <td class="py-3 text-right">
                <button
                  onclick={(e) => { e.stopPropagation(); deleteWorkout(workout.id) }}
                  class="text-red-400 hover:text-red-600 text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="flex justify-end gap-2 mt-4">
      <button
        onclick={exportCsv}
        class="text-xs text-gray-400 hover:text-gray-600 font-medium"
      >
        Export CSV
      </button>
    </div>

    <Pagination {offset} {limit} total={cardio.total} onpagechange={(o: number) => offset = o} onlimitchange={handleLimitChange} />
  {/if}
</div>
