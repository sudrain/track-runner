<script lang="ts">
  import { currentRoute, navigate } from '../router'
  import { auth } from '../stores/auth.svelte'

  let route = $derived($currentRoute)
  let mobileOpen = $state(false)

  function nav(to: string, opts?: { id?: number }) {
    mobileOpen = false
    navigate(to, opts)
  }
</script>

<nav class="bg-indigo-700 text-white shadow-lg">
  <div class="max-w-5xl mx-auto px-4 flex items-center justify-between h-14">
    <button class="text-lg font-bold tracking-tight" onclick={() => nav('home')}>
      Track Runner
    </button>

    <div class="hidden md:flex gap-4 items-center text-sm">
      {#if auth.user}
        <span class="text-indigo-200 truncate max-w-32">{auth.user.email}</span>
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

    <button
      class="md:hidden text-2xl p-1"
      onclick={() => mobileOpen = !mobileOpen}
      aria-label="Menu"
    >
      {mobileOpen ? '✕' : '☰'}
    </button>
  </div>

  {#if mobileOpen}
    <div class="md:hidden border-t border-indigo-600 bg-indigo-700 text-sm">
      {#if auth.user}
        <div class="px-4 py-2 text-indigo-200 truncate">{auth.user.email}</div>
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600 {route.name === 'home' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('home')}
        >
          Stats
        </button>
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600 {route.name === 'cardio' || route.name === 'cardio-new' || route.name === 'cardio-detail' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('cardio')}
        >
          Cardio
        </button>
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600 {route.name === 'strength' || route.name === 'strength-new' || route.name === 'strength-detail' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('strength')}
        >
          Strength
        </button>
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600"
          onclick={() => { mobileOpen = false; auth.logout() }}
        >
          Logout
        </button>
      {:else}
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600 {route.name === 'login' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('login')}
        >
          Login
        </button>
        <button
          class="w-full text-left px-4 py-2 hover:bg-indigo-600 {route.name === 'register' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('register')}
        >
          Register
        </button>
      {/if}
    </div>
  {/if}
</nav>
