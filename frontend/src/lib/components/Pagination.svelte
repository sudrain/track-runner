<script lang="ts">
  let {
    offset = 0,
    limit = 50,
    total = 0,
    onpagechange = (_offset: number) => {},
  } = $props()

  let currentPage = $derived(Math.floor(offset / limit) + 1)
  let totalPages = $derived(Math.ceil(total / limit) || 1)
</script>

{#if totalPages > 1}
  <div class="flex items-center justify-center gap-2 mt-6 text-sm">
    <button
      disabled={currentPage === 1}
      onclick={() => onpagechange(0)}
      class="px-3 py-1 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
    >
      First
    </button>
    <button
      disabled={currentPage === 1}
      onclick={() => onpagechange((currentPage - 2) * limit)}
      class="px-3 py-1 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
    >
      Prev
    </button>

    <span class="text-gray-600 px-2">
      Page {currentPage} of {totalPages}
    </span>

    <button
      disabled={currentPage === totalPages}
      onclick={() => onpagechange(currentPage * limit)}
      class="px-3 py-1 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
    >
      Next
    </button>
    <button
      disabled={currentPage === totalPages}
      onclick={() => onpagechange((totalPages - 1) * limit)}
      class="px-3 py-1 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
    >
      Last
    </button>
  </div>
{/if}
