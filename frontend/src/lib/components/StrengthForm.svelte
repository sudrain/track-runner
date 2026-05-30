<script lang="ts">
  import type { StrengthWorkoutOut, StrengthWorkoutCreate, ExerciseOut } from '../stores/workouts.svelte'
  import { strength } from '../stores/workouts.svelte'
  import { toDatetimeLocal, fromDatetimeLocal } from '../utils/format'

  let {
    workout,
    onsubmit,
    oncancel,
    saving = false,
  } = $props<{
    workout?: StrengthWorkoutOut
    onsubmit: (data: StrengthWorkoutCreate) => void | Promise<void>
    oncancel?: () => void
    saving?: boolean
  }>()

  let datetime = $state('')
  let notes = $state('')
  let exercises = $state<Array<{ name: string; sets: Array<{ weight_kg: string; repetitions: string }> }>>([{ name: '', sets: [{ weight_kg: '', repetitions: '' }] }])

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
      const now = new Date()
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
      datetime = now.toISOString().slice(0, 16)
      notes = ''
    }
  })

  $effect(() => { strength.fetchTemplates('strength') })

  function addExercise() {
    exercises = [...exercises, { name: '', sets: [{ weight_kg: '', repetitions: '' }] }]
  }

  function removeExercise(index: number) {
    exercises = exercises.filter((_, i) => i !== index)
  }

  function addSet(exIndex: number) {
    exercises = exercises.map((ex, i) =>
      i === exIndex
        ? { ...ex, sets: [...ex.sets, { weight_kg: '', repetitions: '' }] }
        : ex
    )
  }

  function removeSet(exIndex: number, setIndex: number) {
    exercises = exercises.map((ex, i) =>
      i === exIndex
        ? { ...ex, sets: ex.sets.filter((_, j) => j !== setIndex) }
        : ex
    )
  }

  function updateSet(exIndex: number, setIndex: number, field: 'weight_kg' | 'repetitions', value: string) {
    exercises = exercises.map((ex, ei) =>
      ei === exIndex
        ? { ...ex, sets: ex.sets.map((s, si) =>
            si === setIndex ? { ...s, [field]: value } : s
          )}
        : ex
    )
  }

  function updateExerciseName(exIndex: number, value: string) {
    exercises = exercises.map((ex, i) => i === exIndex ? { ...ex, name: value } : ex)
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

  let valid = $derived(datetime && exercises.some(ex => ex.name && ex.sets.some(s => parseFloat(s.weight_kg) > 0 && parseInt(s.repetitions) > 0)))
</script>

<form onsubmit={handleSubmit} class="space-y-4">
  <input
    id="strength-datetime"
    type="datetime-local"
    bind:value={datetime}
    required
    class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
  />

  <div>
    {#each exercises as exercise, exIndex}
      <div class="border border-gray-200 rounded-lg px-4 py-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex-1 mr-2">
            {#if strength.templatesLoading}
              <select disabled class="w-full border border-gray-300 rounded px-3 py-5 sm:py-4 text-lg bg-gray-100 text-gray-400">
                <option>Loading...</option>
              </select>
            {:else}
              <select
                id="exercise-name-{exIndex}"
                value={exercise.name}
                onchange={(e) => updateExerciseName(exIndex, (e.target as HTMLSelectElement).value)}
                class="w-full border border-gray-300 rounded px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
              >
                <option value="" disabled>Select exercise...</option>
                {#each strength.templates as tpl (tpl.id)}
                  <option value={tpl.name}>{tpl.name}</option>
                {/each}
              </select>
            {/if}
          </div>
          <button
            type="button"
            onclick={() => removeExercise(exIndex)}
            disabled={exercises.length === 1}
            class="text-red-400 hover:text-red-600 text-2xl font-bold w-10 flex-shrink-0 text-center pb-1 disabled:opacity-20"
          >
            ×
          </button>
        </div>

        <div class="space-y-0.5">
          {#each exercise.sets as set, setIndex}
            <div class="flex items-end justify-between gap-1.5 md:gap-2">
              <div class="flex gap-1.5 md:gap-2 min-w-0">
                <div class="w-20 md:flex-1 md:min-w-[140px]">
                  <label for="weight-{exIndex}-{setIndex}" class="block text-base text-gray-500 mb-0.5">Wt,kg</label>
                    <input
                      id="weight-{exIndex}-{setIndex}"
                      type="number"
                      step="0.5"
                      min="0"
                      value={set.weight_kg}
                      oninput={(e) => updateSet(exIndex, setIndex, 'weight_kg', (e.target as HTMLInputElement).value)}
                      placeholder="80"
                      class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    />
                </div>
                <div class="w-16 md:flex-1 md:min-w-[100px]">
                  <label for="reps-{exIndex}-{setIndex}" class="block text-base text-gray-500 mb-0.5">Reps</label>
                    <input
                      id="reps-{exIndex}-{setIndex}"
                      type="number"
                      min="1"
                      value={set.repetitions}
                      oninput={(e) => updateSet(exIndex, setIndex, 'repetitions', (e.target as HTMLInputElement).value)}
                      placeholder="10"
                      class="w-full border border-gray-300 rounded px-2 md:px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    />
                </div>
              </div>
              <button
                type="button"
                onclick={() => removeSet(exIndex, setIndex)}
                disabled={exercise.sets.length === 1}
                class="text-red-400 hover:text-red-600 text-2xl font-bold w-10 flex-shrink-0 text-center pb-1 disabled:opacity-20"
              >
                ×
              </button>
            </div>
          {/each}
          <div class="flex justify-start">
            <button type="button" onclick={() => addSet(exIndex)} class="bg-indigo-600 text-white rounded-lg px-4 py-2.5 text-base font-medium hover:bg-indigo-700">
              + Add set
            </button>
          </div>
        </div>
      </div>
    {/each}
      <div class="flex justify-start">
        <button type="button" onclick={addExercise} class="bg-indigo-600 text-white rounded-lg px-4 py-2.5 text-base font-medium hover:bg-indigo-700">
          + Add exercise
        </button>
      </div>
      <textarea
        id="strength-notes"
        bind:value={notes}
        rows="2"
        class="w-full border border-gray-300 rounded-lg px-3 py-5 sm:py-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 resize-none min-h-[56px]"
      ></textarea>
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
