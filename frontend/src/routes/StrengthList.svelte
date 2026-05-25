<script lang="ts">
  import { strength } from '../lib/stores/workouts.svelte'
  import { navigate } from '../lib/router'
  import Pagination from '../lib/components/Pagination.svelte'
  import { formatDateShort } from '../lib/utils/format'
  import { showConfirm } from '../lib/stores/confirm.svelte'
  import { showToast } from '../lib/stores/toast.svelte'

  let offset = $state(0)
  let limit = $state(20)
  type SortCol = 'date' | 'exercises' | 'sets' | 'volume'
  let sortCol = $state<SortCol>('date')
  let sortDir = $state<'asc' | 'desc'>('desc')

  $effect(() => {
    strength.fetchList(offset, limit)
  })

  function toggleSort(col: SortCol) {
    if (sortCol === col) {
      sortDir = sortDir === 'asc' ? 'desc' : 'asc'
    } else {
      sortCol = col
      sortDir = 'desc'
    }
  }

  function sortKey(w: typeof strength.list[number]): number | string {
    switch (sortCol) {
      case 'date': return w.datetime
      case 'exercises': return w.exercises.length
      case 'sets': return totalSets(w.exercises)
      case 'volume': return totalVolume(w.exercises)
    }
  }

  let sorted = $derived(
    [...strength.list].sort((a, b) => {
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
    const rows = strength.list.map(w => {
      const exercises = w.exercises.map(e => e.name).join('; ')
      return `${formatDateShort(w.datetime)},"${exercises}",${totalSets(w.exercises)},${totalVolume(w.exercises).toFixed(0)}`
    })
    const csv = 'Date,Exercises,Sets,Volume (kg)\n' + rows.join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'strength-workouts.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  function goToDetail(id: number) {
    navigate('strength-detail', { id })
  }

  async function deleteWorkout(id: number) {
    const ok = await showConfirm('Delete this workout?')
    if (!ok) return
    try {
      await strength.remove(id)
      showToast('Workout deleted')
      strength.fetchList(offset, limit)
    } catch {
      showToast('Failed to delete workout', 'error')
    }
  }

  function totalVolume(exercises: { sets: { weight_kg: number; repetitions: number }[] }[]): number {
    return exercises.reduce((s, ex) => s + ex.sets.reduce((ss, set) => ss + set.weight_kg * set.repetitions, 0), 0)
  }

  function totalSets(exercises: { sets: unknown[] }[]): number {
    return exercises.reduce((s, ex) => s + ex.sets.length, 0)
  }
</script>

<div>
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Strength Workouts</h1>
    <button
      onclick={() => navigate('strength-new')}
      class="bg-indigo-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-indigo-700"
    >
      + New Workout
    </button>
  </div>

  {#if strength.loading}
    <div class="text-gray-400 text-center py-12">Loading...</div>
  {:else if strength.error}
    <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3">{strength.error}</div>
  {:else if strength.list.length === 0}
    <div class="text-gray-400 text-center py-12">No workouts yet. Create your first one!</div>
  {:else}
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-200 text-left text-gray-500">
            <th onclick={() => toggleSort('date')} class="pb-3 font-medium cursor-pointer hover:text-gray-700 select-none">Date{sortIcon('date')}</th>
            <th onclick={() => toggleSort('exercises')} class="pb-3 font-medium cursor-pointer hover:text-gray-700 select-none">Exercises{sortIcon('exercises')}</th>
            <th onclick={() => toggleSort('sets')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">Sets{sortIcon('sets')}</th>
            <th onclick={() => toggleSort('volume')} class="pb-3 font-medium text-right cursor-pointer hover:text-gray-700 select-none">Volume (kg){sortIcon('volume')}</th>
            <th class="pb-3 font-medium text-right"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          {#each sorted as workout}
            <tr class="hover:bg-gray-50 cursor-pointer" onclick={() => goToDetail(workout.id)}>
              <td class="py-3 text-gray-700">{formatDateShort(workout.datetime)}</td>
              <td class="py-3 text-gray-800">{workout.exercises.map(e => e.name).join(', ')}</td>
              <td class="py-3 text-right text-gray-700">{totalSets(workout.exercises)}</td>
              <td class="py-3 text-right text-gray-700">{totalVolume(workout.exercises).toFixed(0)}</td>
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

    <Pagination {offset} {limit} total={strength.total} onpagechange={(o: number) => offset = o} onlimitchange={handleLimitChange} />
  {/if}
</div>
