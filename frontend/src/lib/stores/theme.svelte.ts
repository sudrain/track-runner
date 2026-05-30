function getInitial(): boolean {
  if (typeof localStorage === 'undefined') return false
  const stored = localStorage.getItem('theme')
  if (stored !== null) return stored === 'dark'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function apply(value: boolean) {
  document.documentElement.classList.toggle('dark', value)
  localStorage.setItem('theme', value ? 'dark' : 'light')
}

class ThemeStore {
  isDark = $state(getInitial())

  constructor() {
    apply(this.isDark)
  }

  toggle() {
    this.isDark = !this.isDark
    apply(this.isDark)
  }
}

export const theme = new ThemeStore()
