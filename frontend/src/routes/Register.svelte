<script lang="ts">
  import { auth } from '../lib/stores/auth.svelte'

  let email = $state('')
  let password = $state('')
  let confirm = $state('')
  let localError = $state<string | null>(null)

  async function handleSubmit(e: Event) {
    e.preventDefault()
    localError = null

    if (password !== confirm) {
      localError = 'Пароли не совпадают'
      return
    }

    try {
      await auth.register(email, password)
    } catch {}
  }

  let err = $derived(localError ?? auth.error)
</script>

<div class="max-w-sm mx-auto mt-12">
  <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6 text-center">Регистрация</h1>

  <form onsubmit={handleSubmit} class="space-y-5">
    {#if err}
      <p class="text-red-600 dark:text-red-400 text-base bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded px-4 py-3">{err}</p>
    {/if}

    <div>
      <label for="email" class="block text-base font-medium text-gray-700 dark:text-gray-300 mb-1.5">Email</label>
      <input
        id="email"
        type="email"
        bind:value={email}
        required
        class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-3.5 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-gray-800 dark:text-gray-100"
      />
    </div>

    <div>
      <label for="password" class="block text-base font-medium text-gray-700 dark:text-gray-300 mb-1.5">Пароль</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        required
        minlength={6}
        class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-3.5 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-gray-800 dark:text-gray-100"
      />
    </div>

    <div>
      <label for="confirm" class="block text-base font-medium text-gray-700 dark:text-gray-300 mb-1.5">Подтвердите пароль</label>
      <input
        id="confirm"
        type="password"
        bind:value={confirm}
        required
        class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-3.5 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-gray-800 dark:text-gray-100"
      />
    </div>

    <button
      type="submit"
      disabled={auth.loading}
      class="w-full bg-indigo-600 text-white rounded-lg px-4 py-3.5 text-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {auth.loading ? 'Загрузка...' : 'Зарегистрироваться'}
    </button>
  </form>

  <p class="text-base text-gray-500 dark:text-gray-400 text-center mt-5">
    Уже есть аккаунт?
    <a href="#/login" class="text-indigo-600 dark:text-indigo-400 hover:underline">Войти</a>
  </p>
</div>
