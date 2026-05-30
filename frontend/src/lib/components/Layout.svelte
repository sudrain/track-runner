<script>
  import Navbar from './Navbar.svelte'
  import TabBar from './TabBar.svelte'
  let { children } = $props()
</script>

<div class="min-h-screen bg-gray-50">
  <Navbar />
  <main class="max-w-5xl mx-auto px-0 py-4 sm:py-6 pb-20 md:pb-6">
    {@render children()}
  </main>
  <TabBar />
</div>
