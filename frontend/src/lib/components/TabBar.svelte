<script lang="ts">
  import { currentRoute, navigate } from '../router'
  import { auth } from '../stores/auth.svelte'

  let route = $derived($currentRoute)

  function isActive(names: string[]): boolean {
    return names.includes(route.name)
  }

  const tabs = [
    {
      label: 'Home',
      names: ['home'],
      icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`,
      action: () => navigate('home'),
    },
    {
      label: 'Cardio',
      names: ['cardio', 'cardio-new', 'cardio-detail'],
      icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`,
      action: () => navigate('cardio'),
    },
    {
      label: 'Strength',
      names: ['strength', 'strength-new', 'strength-detail'],
      icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
      action: () => navigate('strength'),
    },
  ]
</script>

{#if auth.user}
  <nav class="fixed bottom-0 left-0 right-0 z-50 md:hidden bg-white border-t border-gray-200 pb-[env(safe-area-inset-bottom,0px)]">
    <div class="flex items-center justify-around h-16">
      {#each tabs as tab}
        <button
          onclick={tab.action}
          class="flex flex-col items-center justify-center gap-0.5 w-full h-full
                 {isActive(tab.names) ? 'text-indigo-600' : 'text-gray-400 hover:text-gray-600'}"
        >
          {@html tab.icon}
          <span class="text-xs font-medium">{tab.label}</span>
        </button>
      {/each}
    </div>
  </nav>
{/if}
