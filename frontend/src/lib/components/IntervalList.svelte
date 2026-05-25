<script lang="ts">
  import type { CardioIntervalOut } from '../stores/workouts.svelte'
  import { formatTempoShort } from '../utils/tempo'

  let { intervals = [] as CardioIntervalOut[] } = $props()
</script>

{#if intervals.length === 0}
  <p class="text-gray-400 text-sm">No intervals</p>
{:else}
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-gray-200 text-left text-gray-500 text-xs">
        <th class="pb-1 font-medium w-6">#</th>
        <th class="pb-1 font-medium">Duration (min)</th>
        <th class="pb-1 font-medium">Distance (km)</th>
        <th class="pb-1 font-medium">Tempo (/km)</th>
        <th class="pb-1 font-medium">HR (bpm)</th>
      </tr>
    </thead>
    <tbody>
      {#each intervals as interval, i}
        <tr class="border-b border-gray-50 text-gray-700">
          <td class="py-1.5 text-gray-400">{i + 1}</td>
          <td class="py-1.5">{interval.duration_minutes.toFixed(1)}</td>
          <td class="py-1.5">{interval.distance_km.toFixed(2)}</td>
          <td class="py-1.5">{formatTempoShort(interval.tempo_min_per_km)}</td>
          <td class="py-1.5">{interval.avg_heart_rate ?? '—'}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
