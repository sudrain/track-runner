<script lang="ts">
  import { strength, type StrengthWorkoutCreate } from '../lib/stores/workouts.svelte'
  import { ApiError } from '../lib/api/client'
  import { navigate } from '../lib/router'
  import StrengthForm from '../lib/components/StrengthForm.svelte'
  import ExerciseList from '../lib/components/ExerciseList.svelte'
  import Skeleton from '../lib/components/Skeleton.svelte'
  import { formatDateShort } from '../lib/utils/format'
  import { showConfirm } from '../lib/stores/confirm.svelte'
  import { showToast } from '../lib/stores/toast.svelte'

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
      await strength.remove(id)
      showToast('Workout deleted')
      navigate('strength')
    } catch {
      showToast('Failed to delete workout', 'error')
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
  <button onclick={() => navigate('strength')} class="text-base text-indigo-600 hover:text-indigo-800 mb-4 block">
    ← Back to list
  </button>

  {#if strength.currentLoading}
    <div class="space-y-4">
      <Skeleton class="h-4 w-32" />
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6 space-y-3">
        <Skeleton class="h-7 w-48" />
        <Skeleton class="h-4 w-36" />
        <div class="flex gap-6 mt-4">
          <Skeleton class="h-10 w-20" />
          <Skeleton class="h-10 w-16" />
          <Skeleton class="h-10 w-24" />
        </div>
        <Skeleton class="h-5 w-28 mt-4" />
        <div class="space-y-2">
          <Skeleton class="h-16 w-full rounded-lg" />
          <Skeleton class="h-16 w-full rounded-lg" />
        </div>
      </div>
    </div>
  {:else if strength.error}
    <div class="text-red-600 text-base bg-red-50 border border-red-200 rounded px-4 py-3">{strength.error}</div>
  {:else if w}
    {#if editing}
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Edit Workout</h1>

      {#if error}
        <div class="text-red-600 text-base bg-red-50 border border-red-200 rounded px-4 py-3 mb-4">{error}</div>
      {/if}

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <StrengthForm workout={w} {saving} onsubmit={handleSave} oncancel={handleCancelEdit} />
      </div>
    {:else}
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-800">Strength Workout</h1>
            <p class="text-base text-gray-500 mt-1">{formatDateShort(w.datetime)}</p>
          </div>
          <div class="flex gap-3">
            <button
              onclick={() => editing = true}
              class="text-base text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Edit
            </button>
            <button
              onclick={handleDelete}
              class="text-base text-red-500 hover:text-red-700 font-medium"
            >
              Delete
            </button>
          </div>
        </div>

        {#if w.notes}
          <p class="text-base text-gray-600 mb-4 whitespace-pre-wrap">{w.notes}</p>
        {/if}

        <div class="flex gap-6 mb-4 text-lg">
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
          <h3 class="text-base font-medium text-gray-700 mb-2">Exercises ({w.exercises.length})</h3>
          <ExerciseList exercises={w.exercises} />
        </div>
      </div>
    {/if}

  {/if}
</div>
