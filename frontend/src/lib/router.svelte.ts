export type Route =
  | { name: 'home' }
  | { name: 'login' }
  | { name: 'register' }
  | { name: 'cardio' }
  | { name: 'cardio-new' }
  | { name: 'cardio-detail'; id: number }
  | { name: 'strength' }
  | { name: 'strength-new' }
  | { name: 'strength-detail'; id: number }

class RouterState {
  current = $state<Route>(parseHash())
}

export const route = new RouterState()

export function navigate(name: Route['name'], data?: Record<string, string | number>) {
  const paths: Record<string, string> = {
    home: '/',
    login: '/login',
    register: '/register',
    cardio: '/cardio',
    'cardio-new': '/cardio/new',
    strength: '/strength',
    'strength-new': '/strength/new',
  }
  let path = paths[name]
  if (!path) {
    if (name === 'cardio-detail') path = `/cardio/${data?.id}`
    else if (name === 'strength-detail') path = `/strength/${data?.id}`
    else path = '/'
  }
  window.location.hash = path
}

export function parseHash(): Route {
  const hash = window.location.hash.replace('#', '') || '/'
  const parts = hash.split('/').filter(Boolean)

  if (parts[0] === 'login') return { name: 'login' }
  if (parts[0] === 'register') return { name: 'register' }
  if (parts[0] === 'cardio') {
    if (parts[1] === 'new') return { name: 'cardio-new' }
    if (parts[1]) {
      const id = Number(parts[1])
      if (!isNaN(id)) return { name: 'cardio-detail', id }
    }
    return { name: 'cardio' }
  }
  if (parts[0] === 'strength') {
    if (parts[1] === 'new') return { name: 'strength-new' }
    if (parts[1]) {
      const id = Number(parts[1])
      if (!isNaN(id)) return { name: 'strength-detail', id }
    }
    return { name: 'strength' }
  }
  return { name: 'home' }
}
