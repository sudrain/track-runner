<script lang="ts">
  import { auth } from '../lib/stores/auth.svelte'
</script>

<div class="text-center py-16">
  <h1 class="text-4xl font-bold text-gray-800 mb-4">Track Runner</h1>
  <p class="text-gray-500 text-lg mb-8">Your workout diary</p>

  {#if auth.user}
    <p class="text-green-600 font-medium">You are logged in as {auth.user.email}</p>
  {:else}
    <div class="flex gap-4 justify-center">
      <a
        href="#/login"
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
      >
        Login
      </a>
      <a
        href="#/register"
        class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
      >
        Register
      </a>
    </div>
  {/if}
</div>
