<script lang="ts">
  import { cardio, type CardioIntervalOut } from '../lib/stores/workouts.svelte'
  import { navigate } from '../lib/router'
  import Pagination from '../lib/components/Pagination.svelte'
  import { formatDateShort } from '../lib/utils/format'
  import { formatTempoShort } from '../lib/utils/tempo'

  let offset = $state(0)
  let limit = 20

  $effect(() => {
    cardio.fetchList(offset, limit)
  })

  function goToDetail(id: number) {
    navigate('cardio-detail', { id })
  }

  async function deleteWorkout(id: number) {
    if (confirm('Delete this workout?')) {
      await cardio.remove(id)
      cardio.fetchList(offset, limit)
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
            <th class="pb-3 font-medium">Name</th>
            <th class="pb-3 font-medium">Date</th>
            <th class="pb-3 font-medium text-right">Distance (km)</th>
            <th class="pb-3 font-medium text-right">Duration (min)</th>
            <th class="pb-3 font-medium text-right">Tempo (/km)</th>
            <th class="pb-3 font-medium text-right">HR (bpm)</th>
            <th class="pb-3 font-medium text-right"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          {#each cardio.list as workout}
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

    <Pagination {offset} {limit} total={cardio.total} onpagechange={(o: number) => offset = o} />
  {/if}
</div>
