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

export function parseTempo(value: string): number | null {
  const trimmed = value.trim()
  if (!trimmed) return null
  if (trimmed.includes(':')) {
    const parts = trimmed.split(':')
    if (parts.length !== 2) return null
    const min = parseInt(parts[0], 10)
    const sec = parseInt(parts[1], 10)
    if (isNaN(min) || isNaN(sec)) return null
    return min + sec / 60
  }
  const num = parseFloat(trimmed)
  return isNaN(num) ? null : num
}

export function formatTempoNumber(tempo: number): string {
  if (tempo <= 0) return ''
  const totalSec = Math.round(tempo * 60)
  const min = Math.floor(totalSec / 60)
  const sec = totalSec % 60
  return `${min}:${sec.toString().padStart(2, '0')}`
}

export function computeTempo(durationMinutes: number, distanceKm: number): number | null {
  if (distanceKm <= 0) return null
  return durationMinutes / distanceKm
}
