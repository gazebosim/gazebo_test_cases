export function getNumber(text: string) {
  const match = text.match(/\d+/)
  if (!match) {
    return 0
  }
  return Number(match[0])
}
