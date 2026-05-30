<script lang="ts">
  import type { CardioWorkoutOut, CardioWorkoutCreate, CardioIntervalOut } from '../stores/workouts.svelte'
  import { cardio } from '../stores/workouts.svelte'
  import { toDatetimeLocal, fromDatetimeLocal } from '../utils/format'
  import { parseTempo, computeTempo, formatTempoNumber } from '../utils/tempo'

  let {
    workout,
    onsubmit,
    oncancel,
    saving = false,
  } = $props<{
    workout?: CardioWorkoutOut
    onsubmit: (data: CardioWorkoutCreate) => void | Promise<void>
    oncancel?: () => void
    saving?: boolean
  }>()

  let name = $state('')
  let datetime = $state('')
  let notes = $state('')
  let intervals = $state<Array<{ duration_minutes: string; distance_km: string; tempo: string; avg_heart_rate: string }>>([])

  function mapIntervals(intervals: CardioIntervalOut[]) {
    return intervals.map(i => ({
      duration_minutes: String(i.duration_minutes),
      distance_km: String(i.distance_km),
      tempo: i.tempo_min_per_km !== null && i.tempo_min_per_km !== undefined ? formatTempoNumber(i.tempo_min_per_km) : '',
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
      const now = new Date()
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
      datetime = now.toISOString().slice(0, 16)
      notes = ''
      intervals = [{ duration_minutes: '', distance_km: '', tempo: '', avg_heart_rate: '' }]
    }
  })

  $effect(() => { cardio.fetchTemplates() })

  function addInterval() {
    intervals = [...intervals, { duration_minutes: '', distance_km: '', tempo: '', avg_heart_rate: '' }]
  }

  function removeInterval(index: number) {
    intervals = intervals.filter((_, i) => i !== index)
  }

  function computedTempo(i: typeof intervals[number]): string {
    const d = parseFloat(i.duration_minutes)
    const dist = parseFloat(i.distance_km)
    if (!d || !dist) return ''
    const t = computeTempo(d, dist)
    return t !== null ? formatTempoNumber(t) : ''
  }

  function handleSubmit(e: Event) {
    e.preventDefault()
    const parsed: CardioWorkoutCreate = {
      name,
      datetime: fromDatetimeLocal(datetime),
      notes,
      intervals: intervals
        .filter(i => i.duration_minutes && i.distance_km)
        .map(i => {
          const tempoParsed = parseTempo(i.tempo)
          return {
            duration_minutes: parseFloat(i.duration_minutes),
            distance_km: parseFloat(i.distance_km),
            ...(tempoParsed !== null ? { tempo_min_per_km: tempoParsed } : {}),
            ...(i.avg_heart_rate ? { avg_heart_rate: parseInt(i.avg_heart_rate, 10) } : {}),
          }
        }),
    }
    if (parsed.intervals.length === 0) return
    onsubmit(parsed)
  }

  let valid = $derived(name && datetime && intervals.some(i => parseFloat(i.duration_minutes) > 0 && parseFloat(i.distance_km) > 0))
</script>

  <form onsubmit={handleSubmit} class="space-y-4">
  {#if cardio.templatesLoading}
    <select disabled class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg bg-gray-100 text-gray-400">
      <option>Loading...</option>
    </select>
  {:else}
    <select
      id="cardio-name"
      bind:value={name}
      required
      class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
    >
      <option value="" disabled>Select workout type...</option>
      {#each cardio.templates as tpl (tpl.id)}
        <option value={tpl.name}>{tpl.name}</option>
      {/each}
    </select>
  {/if}

  <input
    id="cardio-datetime"
    type="datetime-local"
    bind:value={datetime}
    required
    class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
  />

  <div>
    <div class="space-y-0.5">
      {#each intervals as interval, i}
        <div class="flex items-end gap-1.5 md:gap-2">
          <div class="w-16 md:flex-1 md:min-w-[140px]">
            <label for="duration-{i}" class="block text-base text-gray-500 mb-0.5">Min</label>
            <input
              id="duration-{i}"
              type="number"
              step="0.1"
              min="0"
              bind:value={interval.duration_minutes}
              placeholder="30"
              class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div class="w-20 md:flex-1 md:min-w-[140px]">
            <label for="distance-{i}" class="block text-base text-gray-500 mb-0.5">Km</label>
            <input
              id="distance-{i}"
              type="number"
              step="0.01"
              min="0"
              bind:value={interval.distance_km}
              placeholder="5.0"
              class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div class="w-20 md:w-28">
            <label for="tempo-{i}" class="block text-base text-gray-500 mb-0.5">Tempo</label>
            <input
              id="tempo-{i}"
              type="text"
              bind:value={interval.tempo}
              placeholder={computedTempo(interval) || 'M:SS'}
              class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div class="w-16 md:flex-1 md:min-w-[100px]">
            <label for="hr-{i}" class="block text-base text-gray-500 mb-0.5">HR</label>
            <input
              id="hr-{i}"
              type="number"
              min="0"
              max="250"
              bind:value={interval.avg_heart_rate}
              placeholder="—"
              class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <button
            type="button"
            onclick={() => removeInterval(i)}
            disabled={intervals.length === 1}
            class="text-red-400 hover:text-red-600 text-2xl font-bold w-10 flex-shrink-0 pb-1 disabled:opacity-20"
          >
            ×
          </button>
        </div>
      {/each}
      <div class="flex justify-start">
        <button type="button" onclick={addInterval} class="bg-indigo-600 text-white rounded-lg px-4 py-2.5 text-base font-medium hover:bg-indigo-700">
          + Add interval
        </button>
      </div>
      <textarea
        id="cardio-notes"
        bind:value={notes}
        rows="2"
        class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 resize-none min-h-[56px]"
      ></textarea>
    </div>
  </div>

  <div class="flex gap-3 pt-2">
    <button
      type="submit"
      disabled={!valid || saving}
      class="flex-1 bg-indigo-600 text-white rounded-lg py-4 text-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {saving ? 'Saving...' : 'Save'}
    </button>
    {#if oncancel}
      <button
        type="button"
        onclick={oncancel}
        class="flex-1 bg-gray-100 text-gray-700 rounded-lg py-4 text-lg font-medium hover:bg-gray-200"
      >
        Cancel
      </button>
    {/if}
  </div>
</form>
