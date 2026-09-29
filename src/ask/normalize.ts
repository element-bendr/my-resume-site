const STOP_WORDS = new Set([
  "a", "about", "an", "and", "are", "as", "at", "can", "did", "do", "does", "for", "from",
  "has", "have", "how", "i", "in", "is", "it", "me", "of", "on", "or", "the", "this", "to",
  "was", "what", "when", "where", "which", "who", "with", "would", "vijay",
]);

export function normalizeText(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/\p{M}/gu, "")
    .toLocaleLowerCase("en-US")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .trim()
    .replace(/\s+/gu, " ");
}

export function tokenize(value: string): string[] {
  return normalizeText(value)
    .split(" ")
    .filter((token) => token.length > 1 && !STOP_WORDS.has(token));
}
