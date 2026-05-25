<script lang="ts">
  import Layout from './lib/components/Layout.svelte'
  import Toast from './lib/components/Toast.svelte'
  import ConfirmDialog from './lib/components/ConfirmDialog.svelte'
  import { onMount } from 'svelte'
  import { currentRoute, navigate, parseHash } from './lib/router'
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
    currentRoute.set(parseHash())
  }

  onMount(() => {
    auth.checkAuth()
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  })

  let route = $derived($currentRoute)
</script>

{#if auth.loading}
  <div class="flex items-center justify-center min-h-screen text-gray-400 text-lg">
    Loading...
  </div>
{:else}
  <Toast />
  <ConfirmDialog />
  <Layout>
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
  </Layout>
{/if}
