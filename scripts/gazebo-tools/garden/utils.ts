export function getNumber(text: string) {
  const match = text.match(/\d+/)
  if (!match) {
    throw new Error(`Could not parse text: ${text}`)
  }
  return Number(match[0])
}
