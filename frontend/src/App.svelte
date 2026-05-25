<script>
  import Layout from './lib/components/Layout.svelte'
  import { onMount } from 'svelte'
  import { currentRoute, navigate } from './lib/router'
  import { isAuthenticated, currentUser } from './lib/stores/auth'
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
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  })

  function parseHash() {
    const hash = window.location.hash.replace('#', '') || '/'
    const parts = hash.split('/').filter(Boolean)
    if (parts[0] === 'login') return { name: 'login' }
    if (parts[0] === 'register') return { name: 'register' }
    if (parts[0] === 'cardio') {
      if (parts[1] === 'new') return { name: 'cardio-new' }
      if (parts[1]) return { name: 'cardio-detail', id: Number(parts[1]) }
      return { name: 'cardio' }
    }
    if (parts[0] === 'strength') {
      if (parts[1] === 'new') return { name: 'strength-new' }
      if (parts[1]) return { name: 'strength-detail', id: Number(parts[1]) }
      return { name: 'strength' }
    }
    return { name: 'home' }
  }

  let route = $derived($currentRoute)
</script>

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
