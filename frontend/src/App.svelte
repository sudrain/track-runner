<script lang="ts">
  import Layout from './lib/components/Layout.svelte'
  import Toast from './lib/components/Toast.svelte'
  import ConfirmDialog from './lib/components/ConfirmDialog.svelte'
  import Skeleton from './lib/components/Skeleton.svelte'
  import { onMount } from 'svelte'
  import { fade } from 'svelte/transition'
  import { route as router, parseHash } from './lib/router.svelte'
  import { auth } from './lib/stores/auth.svelte'
  import Home from './routes/Home.svelte'
  import Login from './routes/Login.svelte'
  import Register from './routes/Register.svelte'
  import CardioList from './routes/CardioList.svelte'
  import CardioNew from './routes/CardioNew.svelte'
  import CardioDetail from './routes/CardioDetail.svelte'
  import StrengthList from './routes/StrengthList.svelte'
  import StrengthNew from './routes/StrengthNew.svelte'
  import StrengthDetail from './routes/StrengthDetail.svelte'

  function handleHashChange() {
    router.current = parseHash()
  }

  onMount(() => {
    auth.checkAuth()
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  })

  let route = $derived(router.current)
</script>

{#if auth.loading}
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 p-8 space-y-4">
    <div class="max-w-5xl mx-auto space-y-4">
      <Skeleton class="h-8 w-48" />
      <Skeleton class="h-4 w-full" />
      <Skeleton class="h-4 w-3/4" />
      <Skeleton class="h-4 w-1/2" />
    </div>
  </div>
{:else}
  <Toast />
  <ConfirmDialog />
  <Layout>
    {#key route.name}
      <div transition:fade={{ duration: 120 }}>
    {#if route.name === 'home'}
      <Home />
    {:else if route.name === 'login'}
      <Login />
    {:else if route.name === 'register'}
      <Register />
    {:else if route.name === 'cardio'}
      <CardioList />
    {:else if route.name === 'cardio-new'}
      <CardioNew />
    {:else if route.name === 'cardio-detail'}
      <CardioDetail id={route.id} />
    {:else if route.name === 'strength'}
      <StrengthList />
    {:else if route.name === 'strength-new'}
      <StrengthNew />
    {:else if route.name === 'strength-detail'}
      <StrengthDetail id={route.id} />
    {/if}
      </div>
    {/key}
  </Layout>
{/if}
