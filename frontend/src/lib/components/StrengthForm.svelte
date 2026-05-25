<script lang="ts">
  import type { StrengthWorkoutOut, StrengthWorkoutCreate, ExerciseOut } from '../stores/workouts.svelte'
  import { toDatetimeLocal, fromDatetimeLocal } from '../utils/format'

  let {
    workout,
    onsubmit,
    oncancel,
  } = $props<{
    workout?: StrengthWorkoutOut
    onsubmit: (data: StrengthWorkoutCreate) => void | Promise<void>
    oncancel?: () => void
  }>()

  let datetime = $state('')
  let notes = $state('')
  let exercises = $state<Array<{ name: string; sets: Array<{ weight_kg: string; repetitions: string }> }>>([])

  function mapExercises(exercises: ExerciseOut[]) {
    return exercises.map(ex => ({
      name: ex.name,
      sets: ex.sets.map(s => ({
        weight_kg: String(s.weight_kg),
        repetitions: String(s.repetitions),
      })),
    }))
  }

  $effect(() => {
    if (workout) {
      datetime = toDatetimeLocal(workout.datetime)
      notes = workout.notes
      exercises = mapExercises(workout.exercises)
    } else {
      datetime = ''
      notes = ''
      exercises = [{ name: '', sets: [{ weight_kg: '', repetitions: '' }] }]
    }
  })

  function addExercise() {
    exercises = [...exercises, { name: '', sets: [{ weight_kg: '', repetitions: '' }] }]
  }

  function removeExercise(index: number) {
    exercises = exercises.filter((_, i) => i !== index)
  }

  function addSet(exIndex: number) {
    exercises[exIndex].sets = [...exercises[exIndex].sets, { weight_kg: '', repetitions: '' }]
  }

  function removeSet(exIndex: number, setIndex: number) {
    const ex = exercises[exIndex]
    ex.sets = ex.sets.filter((_, i) => i !== setIndex)
  }

  function handleSubmit(e: Event) {
    e.preventDefault()
    const parsed: StrengthWorkoutCreate = {
      datetime: fromDatetimeLocal(datetime),
      notes,
      exercises: exercises
        .filter(ex => ex.name)
        .map(ex => ({
          name: ex.name,
          sets: ex.sets
            .filter(s => s.weight_kg && s.repetitions)
            .map(s => ({
              weight_kg: parseFloat(s.weight_kg),
              repetitions: parseInt(s.repetitions, 10),
            })),
        })),
    }
    if (parsed.exercises.length === 0 || parsed.exercises.some(ex => ex.sets.length === 0)) return
    onsubmit(parsed)
  }

  let valid = $derived(datetime && exercises.some(ex => ex.name && ex.sets.some(s => s.weight_kg && s.repetitions)))
</script>

<form onsubmit={handleSubmit} class="space-y-4">
  <div>
    <label for="strength-datetime" class="block text-sm font-medium text-gray-700 mb-1">Date & Time</label>
    <input
      id="strength-datetime"
      type="datetime-local"
      bind:value={datetime}
      required
      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
    />
  </div>

  <div>
    <label for="strength-notes" class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
    <textarea
      id="strength-notes"
      bind:value={notes}
      rows="3"
      class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
    ></textarea>
  </div>

  <div>
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm font-medium text-gray-700">Exercises</span>
      <button type="button" onclick={addExercise} class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">
        + Add exercise
      </button>
    </div>

    {#each exercises as exercise, exIndex}
      <div class="border border-gray-200 rounded-lg p-4 mb-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex-1 mr-2">
            <label for="exercise-name-{exIndex}" class="block text-xs text-gray-500 mb-0.5">Exercise name</label>
            <input
              id="exercise-name-{exIndex}"
              type="text"
              bind:value={exercise.name}
              placeholder="Bench Press"
              class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <button
            type="button"
            onclick={() => removeExercise(exIndex)}
            disabled={exercises.length === 1}
            class="text-red-400 hover:text-red-600 text-lg px-1 pb-1 self-end disabled:opacity-20"
          >
            ×
          </button>
        </div>

        <div class="ml-2">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs text-gray-400">Sets</span>
            <button type="button" onclick={() => addSet(exIndex)} class="text-xs text-indigo-600 hover:text-indigo-800">
              + Add set
            </button>
          </div>

          {#each exercise.sets as set, setIndex}
            <div class="flex items-end gap-2 mb-1">
              <div class="flex-1 min-w-[80px]">
                <label for="weight-{exIndex}-{setIndex}" class="block text-xs text-gray-500 mb-0.5">Weight (kg)</label>
                <input
                  id="weight-{exIndex}-{setIndex}"
                  type="number"
                  step="0.5"
                  min="0"
                  bind:value={set.weight_kg}
                  placeholder="80"
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
              <div class="flex-1 min-w-[60px]">
                <label for="reps-{exIndex}-{setIndex}" class="block text-xs text-gray-500 mb-0.5">Reps</label>
                <input
                  id="reps-{exIndex}-{setIndex}"
                  type="number"
                  min="1"
                  bind:value={set.repetitions}
                  placeholder="10"
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
              <button
                type="button"
                onclick={() => removeSet(exIndex, setIndex)}
                disabled={exercise.sets.length === 1}
                class="text-red-400 hover:text-red-600 text-base px-1 pb-1 disabled:opacity-20"
              >
                ×
              </button>
            </div>
          {/each}
        </div>
      </div>
    {/each}
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
