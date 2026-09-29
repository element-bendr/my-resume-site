import { normalizeText } from "./normalize";

const unsupportedTerms = new Set([
  "aws", "certification", "certifications", "certified", "certificate", "certificates", "credential", "credentials",
  "university", "degree", "education", "user", "users", "customer", "customers", "count", "sales", "revenue",
  "roi", "salary", "metric", "metrics", "outcome", "outcomes", "testimonial", "testimonials", "increase",
  "increased", "growth", "percentage", "percent", "private", "internal", "secret", "secrets", "confidential",
  "guess", "guessing", "speculate", "speculation", "estimate", "estimating",
]);

export function hasUnsupportedIntent(question: string): boolean {
  const normalized = normalizeText(question);
  const tokens = new Set(normalized.split(" "));
  if ([...unsupportedTerms].some((term) => tokens.has(term))) return true;

  return /\b(ignore|disregard|override)\b.{0,60}\b(rules?|instructions?|policy|system)\b|\b(system prompt|prompt injection)\b|\b(reveal|dump|expose|exfiltrate|print)\b.{0,50}\b(private|internal|secret|confidential|repository|repo|source code|system prompt)\b/.test(normalized);
}
