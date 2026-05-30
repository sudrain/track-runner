<script lang="ts">
  import { route as router, navigate, type Route } from '../router.svelte'
  import { auth } from '../stores/auth.svelte'
  import { theme } from '../stores/theme.svelte'

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
        <button
          onclick={() => theme.toggle()}
          class="p-2 rounded hover:bg-indigo-600"
          aria-label={theme.isDark ? 'Светлая тема' : 'Тёмная тема'}
        >
          {#if theme.isDark}
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
          {/if}
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
        <button
          onclick={() => { theme.toggle() }}
          class="w-full text-left px-4 py-3 hover:bg-indigo-600 flex items-center gap-2"
        >
          {#if theme.isDark}
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
          {/if}
          {theme.isDark ? 'Светлая тема' : 'Тёмная тема'}
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
