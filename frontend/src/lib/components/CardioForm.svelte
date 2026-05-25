<script lang="ts">
  import type { CardioWorkoutOut, CardioWorkoutCreate, CardioIntervalOut } from '../stores/workouts.svelte'
  import { toDatetimeLocal, fromDatetimeLocal } from '../utils/format'

  let {
    workout,
    onsubmit,
    oncancel,
  } = $props<{
    workout?: CardioWorkoutOut
    onsubmit: (data: CardioWorkoutCreate) => void | Promise<void>
    oncancel?: () => void
  }>()

  let name = $state('')
  let datetime = $state('')
  let notes = $state('')
  let intervals = $state<Array<{ duration_minutes: string; distance_km: string; avg_heart_rate: string }>>([])

  function mapIntervals(intervals: CardioIntervalOut[]) {
    return intervals.map(i => ({
      duration_minutes: String(i.duration_minutes),
      distance_km: String(i.distance_km),
      avg_heart_rate: i.avg_heart_rate ? String(i.avg_heart_rate) : '',
    }))
  }

  $effect(() => {
    if (workout) {
      name = workout.name
      datetime = toDatetimeLocal(workout.datetime)
      notes = workout.notes
      intervals = mapIntervals(workout.intervals)
    } else {
      name = ''
      datetime = ''
      notes = ''
      intervals = [{ duration_minutes: '', distance_km: '', avg_heart_rate: '' }]
    }
  })

  function addInterval() {
    intervals = [...intervals, { duration_minutes: '', distance_km: '', avg_heart_rate: '' }]
  }

  function removeInterval(index: number) {
    intervals = intervals.filter((_, i) => i !== index)
  }

  function intervalTempo(interval: typeof intervals[number]): string {
    const d = parseFloat(interval.duration_minutes)
    const dist = parseFloat(interval.distance_km)
    if (!d || !dist) return ''
    const t = d / dist
    const min = Math.floor(t)
    const sec = Math.round((t - min) * 60)
    return `${min}:${sec.toString().padStart(2, '0')}`
  }

  function handleSubmit(e: Event) {
    e.preventDefault()
    const parsed: CardioWorkoutCreate = {
      name,
      datetime: fromDatetimeLocal(datetime),
      notes,
      intervals: intervals
        .filter(i => i.duration_minutes && i.distance_km)
        .map(i => ({
          duration_minutes: parseFloat(i.duration_minutes),
          distance_km: parseFloat(i.distance_km),
          ...(i.avg_heart_rate ? { avg_heart_rate: parseInt(i.avg_heart_rate, 10) } : {}),
        })),
    }
    if (parsed.intervals.length === 0) return
    onsubmit(parsed)
  }

  let valid = $derived(name && datetime && intervals.some(i => i.duration_minutes && i.distance_km))
</script>

<form onsubmit={handleSubmit} class="space-y-4">
  <div>
    <label for="cardio-name" class="block text-sm font-medium text-gray-700 mb-1">Name</label>
    <input
      id="cardio-name"
      type="text"
      bind:value={name}
      required
      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
    />
  </div>

  <div>
    <label for="cardio-datetime" class="block text-sm font-medium text-gray-700 mb-1">Date & Time</label>
    <input
      id="cardio-datetime"
      type="datetime-local"
      bind:value={datetime}
      required
      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
    />
  </div>

  <div>
    <label for="cardio-notes" class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
    <textarea
      id="cardio-notes"
      bind:value={notes}
      rows="3"
      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
    ></textarea>
  </div>

  <div>
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm font-medium text-gray-700">Intervals</span>
      <button type="button" onclick={addInterval} class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">
        + Add interval
      </button>
    </div>

    <div class="space-y-2">
      {#each intervals as interval, i}
        <div class="flex items-end gap-2">
          <div class="flex-1">
            <label for="duration-{i}" class="block text-xs text-gray-500 mb-0.5">Duration (min)</label>
            <input
              id="duration-{i}"
              type="number"
              step="0.1"
              min="0"
              bind:value={interval.duration_minutes}
              placeholder="30"
              class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div class="flex-1">
            <label for="distance-{i}" class="block text-xs text-gray-500 mb-0.5">Distance (km)</label>
            <input
              id="distance-{i}"
              type="number"
              step="0.01"
              min="0"
              bind:value={interval.distance_km}
              placeholder="5.0"
              class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div class="w-14 text-center pt-5 text-xs text-gray-400">
            {intervalTempo(interval)}
          </div>
          <div class="flex-1">
            <label for="hr-{i}" class="block text-xs text-gray-500 mb-0.5">HR (bpm)</label>
            <input
              id="hr-{i}"
              type="number"
              min="0"
              max="250"
              bind:value={interval.avg_heart_rate}
              placeholder="—"
              class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <button
            type="button"
            onclick={() => removeInterval(i)}
            disabled={intervals.length === 1}
            class="text-red-400 hover:text-red-600 text-lg px-1 pb-1 disabled:opacity-20"
          >
            ×
          </button>
        </div>
      {/each}
    </div>
  </div>

  <div class="flex gap-3 pt-2">
    <button
      type="submit"
      disabled={!valid}
      class="bg-indigo-600 text-white rounded-lg px-5 py-2 text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Save
    </button>
    {#if oncancel}
      <button
        type="button"
        onclick={oncancel}
        class="bg-gray-100 text-gray-700 rounded-lg px-5 py-2 text-sm font-medium hover:bg-gray-200"
      >
        Cancel
      </button>
    {/if}
  </div>
</form>
