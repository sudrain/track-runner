<script lang="ts">
  import { strength, type StrengthWorkoutCreate } from '../lib/stores/workouts.svelte'
  import { ApiError } from '../lib/api/client'
  import { navigate } from '../lib/router'
  import StrengthForm from '../lib/components/StrengthForm.svelte'
  import ExerciseList from '../lib/components/ExerciseList.svelte'
  import { formatDateShort } from '../lib/utils/format'

  let { id } = $props<{ id: number }>()

  let editing = $state(false)
  let saving = $state(false)
  let error = $state<string | null>(null)

  $effect(() => {
    if (id) strength.fetchOne(id)
  })

  async function handleSave(data: StrengthWorkoutCreate) {
    saving = true
    error = null
    try {
      await strength.update(id, data)
      editing = false
    } catch (e) {
      error = e instanceof ApiError ? e.detail : 'Failed to update workout'
    } finally {
      saving = false
    }
  }

  async function handleDelete() {
    if (confirm('Delete this workout?')) {
      await strength.remove(id)
      navigate('strength')
    }
  }

  function handleCancelEdit() {
    editing = false
  }

  let w = $derived(strength.current)
  let totalSets = $derived(w ? w.exercises.reduce((s, ex) => s + ex.sets.length, 0) : 0)
  let totalVolume = $derived(w ? w.exercises.reduce((s, ex) => s + ex.sets.reduce((ss, set) => ss + set.weight_kg * set.repetitions, 0), 0) : 0)
</script>

<div class="max-w-2xl mx-auto">
  <button onclick={() => navigate('strength')} class="text-sm text-indigo-600 hover:text-indigo-800 mb-4 block">
    ← Back to list
  </button>

  {#if strength.currentLoading}
    <div class="text-gray-400 text-center py-12">Loading...</div>
  {:else if strength.error}
    <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3">{strength.error}</div>
  {:else if w}
    {#if editing}
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Edit Workout</h1>

      {#if error}
        <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3 mb-4">{error}</div>
      {/if}

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <StrengthForm workout={w} onsubmit={handleSave} oncancel={handleCancelEdit} />
      </div>
    {:else}
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-800">Strength Workout</h1>
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

        <div class="flex gap-6 mb-4 text-sm">
          <div>
            <span class="text-gray-400">Exercises</span>
            <p class="font-semibold text-gray-800">{w.exercises.length}</p>
          </div>
          <div>
            <span class="text-gray-400">Total sets</span>
            <p class="font-semibold text-gray-800">{totalSets}</p>
          </div>
          <div>
            <span class="text-gray-400">Volume (kg)</span>
            <p class="font-semibold text-gray-800">{totalVolume.toFixed(0)}</p>
          </div>
        </div>

        <div class="border-t border-gray-100 pt-4">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Exercises ({w.exercises.length})</h3>
          <ExerciseList exercises={w.exercises} />
        </div>
      </div>
    {/if}

    {#if saving}
      <div class="text-gray-400 text-sm text-center mt-4">Saving...</div>
    {/if}
  {/if}
</div>
