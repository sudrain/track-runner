<script lang="ts">
  import { getConfirmState, confirmYes, confirmNo } from '../stores/confirm.svelte'

  let state = $derived(getConfirmState())
</script>

{#if state.show}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 dark:bg-black/50"
    onclick={confirmNo}
    onkeydown={(e) => { if (e.key === 'Escape') confirmNo() }}
    role="dialog"
    tabindex="-1"
  >
    <div
      role="none"
      class="bg-white dark:bg-gray-900 rounded-xl shadow-xl p-6 mx-4 max-w-sm w-full"
      onclick={(e) => e.stopPropagation()}
      onkeydown={() => {}}
    >
      <p class="text-gray-800 dark:text-gray-100 text-sm">{state.message}</p>
      <div class="flex justify-end gap-3 mt-6">
        <button
          onclick={confirmNo}
          class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          Отмена
        </button>
        <button
          onclick={confirmYes}
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700"
        >
          Удалить
        </button>
      </div>
    </div>
  </div>
{/if}
