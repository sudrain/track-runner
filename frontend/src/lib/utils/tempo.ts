export function formatTempo(tempo: number | null): string {
  if (tempo === null || tempo === undefined) return '—'
  const totalSec = Math.round(tempo * 60)
  const min = Math.floor(totalSec / 60)
  const sec = totalSec % 60
  return `${min}:${sec.toString().padStart(2, '0')} /km`
}

export function formatTempoShort(tempo: number | null): string {
  if (tempo === null || tempo === undefined) return '—'
  const totalSec = Math.round(tempo * 60)
  const min = Math.floor(totalSec / 60)
  const sec = totalSec % 60
  return `${min}:${sec.toString().padStart(2, '0')}`
}

export function computeTempo(durationMinutes: number, distanceKm: number): number | null {
  if (distanceKm <= 0) return null
  return durationMinutes / distanceKm
}
