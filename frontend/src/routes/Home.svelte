<script lang="ts">
  import { auth } from '../lib/stores/auth.svelte'
  import { stats } from '../lib/stores/stats.svelte'
  import { formatTempoShort } from '../lib/utils/tempo'

  $effect(() => {
    if (auth.user) {
      stats.fetch()
    } else {
      stats.data = null
    }
  })
</script>

{#if auth.user}
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>

    {#if stats.loading}
      <div class="text-gray-400 text-center py-12">Loading statistics...</div>
    {:else if stats.error}
      <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3">{stats.error}</div>
    {:else if stats.data}
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Week</p>
          <p class="text-3xl font-bold text-indigo-600">{stats.data.week_km.toFixed(2)} km</p>
          <p class="text-sm text-gray-400 mt-2">{formatTempoShort(stats.data.week_avg_tempo)} /km</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Month</p>
          <p class="text-3xl font-bold text-indigo-600">{stats.data.month_km.toFixed(2)} km</p>
          <p class="text-sm text-gray-400 mt-2">{formatTempoShort(stats.data.month_avg_tempo)} /km</p>
        </div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Year</p>
          <p class="text-3xl font-bold text-indigo-600">{stats.data.year_km.toFixed(2)} km</p>
          <p class="text-sm text-gray-400 mt-2">{formatTempoShort(stats.data.year_avg_tempo)} /km</p>
        </div>
      </div>
    {/if}
  </div>
{:else}
  <div class="text-center py-16">
    <h1 class="text-4xl font-bold text-gray-800 mb-4">Track Runner</h1>
    <p class="text-gray-500 text-lg mb-8">Your workout diary</p>
    <div class="flex gap-4 justify-center">
      <a
        href="#/login"
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
      >
        Login
      </a>
      <a
        href="#/register"
        class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
      >
        Register
      </a>
    </div>
  </div>
{/if}
