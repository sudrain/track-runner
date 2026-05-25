<script lang="ts">
  import { currentRoute, navigate } from '../router'
  import { auth } from '../stores/auth.svelte'

  let route = $derived($currentRoute)
</script>

<nav class="bg-indigo-700 text-white shadow-lg">
  <div class="max-w-5xl mx-auto px-4 flex items-center justify-between h-14">
    <button
      class="text-lg font-bold tracking-tight"
      onclick={() => navigate('home')}
    >
      Track Runner
    </button>

    <div class="flex gap-4 items-center text-sm">
      {#if auth.user}
        <span class="text-indigo-200">{auth.user.email}</span>
        <button
          class="hover:text-indigo-200 {route.name === 'cardio' || route.name === 'cardio-new' || route.name === 'cardio-detail' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('cardio')}
        >
          Cardio
        </button>
        <button
          class="hover:text-indigo-200 {route.name === 'strength' || route.name === 'strength-new' || route.name === 'strength-detail' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('strength')}
        >
          Strength
        </button>
        <button
          class="hover:text-indigo-200 {route.name === 'home' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('home')}
        >
          Stats
        </button>
        <button
          class="bg-indigo-600 hover:bg-indigo-500 border border-indigo-400 px-3 py-1 rounded"
          onclick={auth.logout}
        >
          Logout
        </button>
      {:else}
        <button
          class="hover:text-indigo-200 {route.name === 'login' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('login')}
        >
          Login
        </button>
        <button
          class="hover:text-indigo-200 {route.name === 'register' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('register')}
        >
          Register
        </button>
      {/if}
    </div>
  </div>
</nav>
