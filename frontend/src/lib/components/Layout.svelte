<script>
  import Navbar from './Navbar.svelte'
  let { children } = $props()
</script>

<div class="min-h-screen bg-gray-50">
  <Navbar />
  <main class="max-w-5xl mx-auto px-4 py-4 sm:py-6">
    {@render children()}
  </main>
</div>
