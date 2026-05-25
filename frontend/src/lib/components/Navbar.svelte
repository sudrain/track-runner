<script lang="ts">
  import { navigate } from '../router'
  import { auth } from '../stores/auth.svelte'
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
        <button class="hover:text-indigo-200" onclick={() => navigate('cardio')}>
          Cardio
        </button>
        <button class="hover:text-indigo-200" onclick={() => navigate('strength')}>
          Strength
        </button>
        <button class="hover:text-indigo-200" onclick={() => navigate('home')}>
          Stats
        </button>
        <button
          class="bg-indigo-600 hover:bg-indigo-500 border border-indigo-400 px-3 py-1 rounded"
          onclick={auth.logout}
        >
          Logout
        </button>
      {:else}
        <button class="hover:text-indigo-200" onclick={() => navigate('login')}>
          Login
        </button>
        <button class="hover:text-indigo-200" onclick={() => navigate('register')}>
          Register
        </button>
      {/if}
    </div>
  </div>
</nav>
