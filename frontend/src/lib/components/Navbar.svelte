<script>
  import { currentRoute, navigate } from '../router'
  import { isAuthenticated } from '../stores/auth'
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
      {#if $isAuthenticated}
        <button class="hover:text-indigo-200" onclick={() => navigate('cardio')}>
          Cardio
        </button>
        <button class="hover:text-indigo-200" onclick={() => navigate('strength')}>
          Strength
        </button>
        <button class="hover:text-indigo-200" onclick={() => navigate('home')}>
          Stats
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
