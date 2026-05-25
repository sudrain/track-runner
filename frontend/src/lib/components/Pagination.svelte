<script lang="ts">
  let {
    offset = 0,
    limit = 20,
    total = 0,
    onpagechange = (_offset: number) => {},
    onlimitchange = (_limit: number) => {},
  } = $props()

  let currentPage = $derived(Math.floor(offset / limit) + 1)
  let totalPages = $derived(Math.ceil(total / limit) || 1)

  function changeLimit(e: Event) {
    const newLimit = parseInt((e.target as HTMLSelectElement).value, 10)
    onlimitchange(newLimit)
  }
</script>

<div class="flex items-center justify-between mt-6 text-base">
  <div class="flex items-center gap-2 text-gray-500">
    <span>Rows:</span>
    <select
      value={limit}
      onchange={changeLimit}
      class="border border-gray-300 rounded px-3 py-1.5 text-base focus:outline-none focus:ring-2 focus:ring-indigo-400"
    >
      <option value={10}>10</option>
      <option value={20}>20</option>
      <option value={50}>50</option>
      <option value={100}>100</option>
    </select>
  </div>

  {#if totalPages > 1}
    <div class="flex items-center gap-2">
      <button
        disabled={currentPage === 1}
        onclick={() => onpagechange(0)}
        class="px-4 py-1.5 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
      >
        First
      </button>
      <button
        disabled={currentPage === 1}
        onclick={() => onpagechange((currentPage - 2) * limit)}
        class="px-4 py-1.5 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
      >
        Prev
      </button>

      <span class="text-gray-600 px-2">
        Page {currentPage} of {totalPages}
      </span>

      <button
        disabled={currentPage === totalPages}
        onclick={() => onpagechange(currentPage * limit)}
        class="px-4 py-1.5 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
      >
        Next
      </button>
      <button
        disabled={currentPage === totalPages}
        onclick={() => onpagechange((totalPages - 1) * limit)}
        class="px-4 py-1.5 rounded border border-gray-300 disabled:opacity-30 hover:bg-gray-100"
      >
        Last
      </button>
    </div>
  {/if}
</div>
