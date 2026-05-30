<script lang="ts">
  let { class: className = '' } = $props<{ class?: string }>()
</script>

<div class="animate-pulse bg-gray-200 rounded {className}"></div>
