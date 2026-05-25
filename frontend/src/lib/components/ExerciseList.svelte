<script lang="ts">
  import type { ExerciseOut } from '../stores/workouts.svelte'

  let { exercises = [] as ExerciseOut[] } = $props()
</script>

{#if exercises.length === 0}
  <p class="text-gray-400 text-sm">No exercises</p>
{:else}
  <div class="space-y-2">
    {#each exercises as exercise}
      <div>
        <p class="text-sm font-medium text-gray-800">{exercise.name}</p>
        <table class="w-full text-sm ml-4 mt-0.5">
          <thead>
            <tr class="text-left text-gray-400 text-xs">
              <th class="w-6 pb-0.5">#</th>
              <th class="pb-0.5">Weight (kg)</th>
              <th class="pb-0.5">Reps</th>
            </tr>
          </thead>
          <tbody>
            {#each exercise.sets as set, i}
              <tr class="text-gray-700">
                <td class="py-0.5 text-gray-400">{i + 1}</td>
                <td class="py-0.5">{set.weight_kg.toFixed(1)}</td>
                <td class="py-0.5">{set.repetitions}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/each}
  </div>
{/if}
