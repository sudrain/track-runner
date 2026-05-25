import { writable } from 'svelte/store'

export const isAuthenticated = writable<boolean>(false)
export const currentUser = writable<{ id: string; email: string } | null>(null)
