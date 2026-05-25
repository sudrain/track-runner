export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDistance(km: number): string {
  if (km >= 1) return `${km.toFixed(2)} km`
  return `${(km * 1000).toFixed(0)} m`
}

export function formatDuration(minutes: number): string {
  const h = Math.floor(minutes / 60)
  const m = Math.round(minutes % 60)
  if (h === 0) return `${m} min`
  return `${h}h ${m}min`
}

export function formatTempo(tempo: number | null): string {
  if (tempo === null || tempo === undefined) return '—'
  const totalSec = Math.round(tempo * 60)
  const min = Math.floor(totalSec / 60)
  const sec = totalSec % 60
  return `${min}:${sec.toString().padStart(2, '0')} /km`
}
