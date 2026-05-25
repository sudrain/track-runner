<script lang="ts">
  import type { CardioIntervalOut } from '../stores/workouts.svelte'
  import { computeTempo, formatTempoShort } from '../utils/tempo'

  let { intervals = [] as CardioIntervalOut[] } = $props()

  function displayTempo(i: CardioIntervalOut): string {
    if (i.tempo_min_per_km !== null) return formatTempoShort(i.tempo_min_per_km)
    return formatTempoShort(computeTempo(i.duration_minutes, i.distance_km))
  }
</script>

{#if intervals.length === 0}
  <p class="text-gray-400 text-base">No intervals</p>
{:else}
  <table class="w-full text-base">
    <thead>
      <tr class="border-b border-gray-200 text-left text-gray-500">
        <th class="pb-1.5 font-medium w-8">#</th>
        <th class="pb-1.5 font-medium">Min</th>
        <th class="pb-1.5 font-medium">Km</th>
        <th class="pb-1.5 font-medium">Tempo</th>
        <th class="pb-1.5 font-medium">HR</th>
      </tr>
    </thead>
    <tbody>
      {#each intervals as interval, i}
        <tr class="border-b border-gray-50 text-gray-700">
          <td class="py-2 text-gray-400">{i + 1}</td>
          <td class="py-2">{interval.duration_minutes.toFixed(1)}</td>
          <td class="py-2">{interval.distance_km.toFixed(2)}</td>
          <td class="py-2">{displayTempo(interval)}</td>
          <td class="py-2">{interval.avg_heart_rate ?? '—'}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
