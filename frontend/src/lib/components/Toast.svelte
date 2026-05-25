<script lang="ts">
  import { getToasts, dismissToast } from '../stores/toast.svelte'

  let toasts = $derived(getToasts())
</script>

{#if toasts.length > 0}
  <div class="fixed top-4 right-4 z-50 space-y-2">
    {#each toasts as toast (toast.id)}
      <div
        class="flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-sm font-medium max-w-sm animate-slide-in"
        class:bg-green-600={toast.type === 'success'}
        class:bg-red-600={toast.type === 'error'}
      >
        <span class="text-white flex-1">{toast.message}</span>
        <button
          onclick={() => dismissToast(toast.id)}
          class="text-white/70 hover:text-white text-lg leading-none"
        >
          ×
        </button>
      </div>
    {/each}
  </div>
{/if}

<style>
  @keyframes slide-in {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  .animate-slide-in {
    animation: slide-in 0.25s ease-out;
  }
</style>
