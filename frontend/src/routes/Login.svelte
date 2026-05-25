<script lang="ts">
  import { auth } from '../lib/stores/auth.svelte'

  let email = $state('')
  let password = $state('')

  async function handleSubmit(e: Event) {
    e.preventDefault()
    try {
      await auth.login(email, password)
    } catch {}
  }
</script>

<div class="max-w-sm mx-auto mt-12">
  <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Login</h1>

  <form onsubmit={handleSubmit} class="space-y-4">
    {#if auth.error}
      <p class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-3 py-2">{auth.error}</p>
    {/if}

    <div>
      <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
      <input
        id="email"
        type="email"
        bind:value={email}
        required
        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>

    <div>
      <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        required
        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>

    <button
      type="submit"
      disabled={auth.loading}
      class="w-full bg-indigo-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {auth.loading ? 'Loading...' : 'Login'}
    </button>
  </form>

  <p class="text-sm text-gray-500 text-center mt-4">
    Don't have an account?
    <a href="#/register" class="text-indigo-600 hover:underline">Register</a>
  </p>
</div>
