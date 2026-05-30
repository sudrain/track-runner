<script lang="ts">
  import { route as router, navigate, type Route } from '../router.svelte'
  import { auth } from '../stores/auth.svelte'

  let route = $derived(router.current)
  let mobileOpen = $state(false)

  function nav(to: Route['name'], opts?: { id?: number }) {
    mobileOpen = false
    navigate(to, opts)
  }
</script>

<nav class="bg-indigo-700 text-white shadow-lg">
  <div class="max-w-5xl mx-auto px-4 flex items-center justify-between h-16">
    <button class="text-xl font-bold tracking-tight" onclick={() => nav('home')}>
      Track Runner
    </button>

    <div class="hidden md:flex gap-5 items-center text-base">
      {#if auth.user}
        <button
          class="hover:text-indigo-200 {route.name === 'cardio' || route.name === 'cardio-new' || route.name === 'cardio-detail' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('cardio')}
        >
          Кардио
        </button>
        <button
          class="hover:text-indigo-200 {route.name === 'strength' || route.name === 'strength-new' || route.name === 'strength-detail' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('strength')}
        >
          Силовая
        </button>
        <button
          class="hover:text-indigo-200 {route.name === 'home' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('home')}
        >
          Статистика
        </button>
        <button
          class="bg-indigo-600 hover:bg-indigo-500 border border-indigo-400 px-4 py-2 rounded"
          onclick={() => auth.logout()}
        >
          Выйти
        </button>
      {:else}
        <button
          class="hover:text-indigo-200 {route.name === 'login' ? 'text-indigo-100 border-b border-indigo-300' : 'text-white'}"
          onclick={() => navigate('login')}
        >
          Войти
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
      class="md:hidden text-3xl p-1"
      onclick={() => mobileOpen = !mobileOpen}
      aria-label="Меню"
    >
      {mobileOpen ? '✕' : '☰'}
    </button>
  </div>

  {#if mobileOpen}
    <div class="md:hidden border-t border-indigo-600 bg-indigo-700 text-base">
      {#if auth.user}
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 {route.name === 'home' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('home')}
        >
          Stats
        </button>
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 {route.name === 'cardio' || route.name === 'cardio-new' || route.name === 'cardio-detail' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('cardio')}
        >
          Cardio
        </button>
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 {route.name === 'strength' || route.name === 'strength-new' || route.name === 'strength-detail' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('strength')}
        >
          Силовая
        </button>
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600"
          onclick={() => { mobileOpen = false; auth.logout() }}
        >
          Выйти
        </button>
      {:else}
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 {route.name === 'login' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('login')}
        >
          Войти
        </button>
        <button
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 {route.name === 'register' ? 'bg-indigo-600' : ''}"
          onclick={() => nav('register')}
        >
          Регистрация
        </button>
      {/if}
    </div>
  {/if}
</nav>
