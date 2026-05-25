<script lang="ts">
  import { cardio, type CardioWorkoutCreate, type CardioIntervalOut } from '../lib/stores/workouts.svelte'
  import { ApiError } from '../lib/api/client'
  import { navigate } from '../lib/router'
  import CardioForm from '../lib/components/CardioForm.svelte'
  import IntervalList from '../lib/components/IntervalList.svelte'
  import { formatDateShort } from '../lib/utils/format'
  import { formatTempoShort } from '../lib/utils/tempo'
  import { showConfirm } from '../lib/stores/confirm.svelte'
  import { showToast } from '../lib/stores/toast.svelte'

  let { id } = $props<{ id: number }>()

  let editing = $state(false)
  let saving = $state(false)
  let error = $state<string | null>(null)

  $effect(() => {
    if (id) cardio.fetchOne(id)
  })

  async function handleSave(data: CardioWorkoutCreate) {
    saving = true
    error = null
    try {
      await cardio.update(id, data)
      showToast('Workout updated')
      editing = false
    } catch (e) {
      error = e instanceof ApiError ? e.detail : 'Failed to update workout'
    } finally {
      saving = false
    }
  }

  async function handleDelete() {
    const ok = await showConfirm('Delete this workout?')
    if (!ok) return
    try {
      await cardio.remove(id)
      showToast('Workout deleted')
      navigate('cardio')
    } catch {
      showToast('Failed to delete workout', 'error')
    }
  }

  function handleCancelEdit() {
    editing = false
  }

  let w = $derived(cardio.current)
  let totalKm = $derived(w ? w.intervals.reduce((s, i) => s + i.distance_km, 0) : 0)
  let totalMin = $derived(w ? w.intervals.reduce((s, i) => s + i.duration_minutes, 0) : 0)
  let tempo = $derived(totalKm > 0 ? totalMin / totalKm : null)
</script>

<div class="max-w-2xl mx-auto">
  <button onclick={() => navigate('cardio')} class="text-sm text-indigo-600 hover:text-indigo-800 mb-4 block">
    ← Back to list
  </button>

  {#if cardio.currentLoading}
    <div class="text-gray-400 text-center py-12">Loading...</div>
  {:else if cardio.error}
    <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3">{cardio.error}</div>
  {:else if w}
    {#if editing}
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Edit: {w.name}</h1>

      {#if error}
        <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3 mb-4">{error}</div>
      {/if}

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 px-2 py-3">
        <CardioForm workout={w} onsubmit={handleSave} oncancel={handleCancelEdit} />
      </div>
    {:else}
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 px-2 py-3">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-800">{w.name}</h1>
            <p class="text-sm text-gray-500 mt-1">{formatDateShort(w.datetime)}</p>
          </div>
          <div class="flex gap-2">
            <button
              onclick={() => editing = true}
              class="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Edit
            </button>
            <button
              onclick={handleDelete}
              class="text-sm text-red-500 hover:text-red-700 font-medium"
            >
              Delete
            </button>
          </div>
        </div>

        {#if w.notes}
          <p class="text-sm text-gray-600 mb-4 whitespace-pre-wrap">{w.notes}</p>
        {/if}

        <div class="flex gap-6 mb-4 text-base">
          <div>
            <span class="text-gray-400">Km</span>
            <p class="font-semibold text-gray-800">{totalKm.toFixed(2)}</p>
          </div>
          <div>
            <span class="text-gray-400">Min</span>
            <p class="font-semibold text-gray-800">{totalMin.toFixed(0)}</p>
          </div>
          <div>
            <span class="text-gray-400">Tempo</span>
            <p class="font-semibold text-gray-800">{formatTempoShort(tempo)}</p>
          </div>
        </div>

        <div class="border-t border-gray-100 pt-4">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Intervals ({w.intervals.length})</h3>
          <IntervalList intervals={w.intervals} />
        </div>
      </div>
    {/if}

    {#if saving}
      <div class="text-gray-400 text-sm text-center mt-4">Saving...</div>
    {/if}
  {/if}
</div>
