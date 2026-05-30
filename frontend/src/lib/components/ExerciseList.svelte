<script lang="ts">
  import type { ExerciseOut } from '../stores/workouts.svelte'

  let { exercises = [] as ExerciseOut[] } = $props()
</script>

{#if exercises.length === 0}
  <p class="text-gray-400 dark:text-gray-500 text-base">Нет упражнений</p>
{:else}
  <div class="space-y-3">
    {#each exercises as exercise}
      <div>
        <p class="text-base font-medium text-gray-800 dark:text-gray-100">{exercise.name}</p>
        <table class="w-full text-base ml-4 mt-1">
          <thead>
            <tr class="text-left text-gray-400 dark:text-gray-500">
              <th class="w-8 pb-1">#</th>
              <th class="pb-1">Вес (кг)</th>
              <th class="pb-1">Повт</th>
            </tr>
          </thead>
          <tbody>
            {#each exercise.sets as set, i}
              <tr class="text-gray-700 dark:text-gray-300">
                <td class="py-1 text-gray-400 dark:text-gray-500">{i + 1}</td>
                <td class="py-1">{set.weight_kg.toFixed(1)}</td>
                <td class="py-1">{set.repetitions}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/each}
  </div>
{/if}
