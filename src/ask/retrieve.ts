import { evidenceRegistry, type EvidenceRecord } from "./evidence";
import { normalizeText, tokenize } from "./normalize";

const MIN_SCORE = 2;
const MAX_MATCHES = 5;

function includesPhrase(query: string, phrase: string): boolean {
  const normalizedPhrase = normalizeText(phrase);
  return normalizedPhrase.length > 0 && ` ${query} `.includes(` ${normalizedPhrase} `);
}

function requestedTechnologies(query: string): Set<string> {
  const matches = new Set(
    evidenceRegistry
      .filter((record) => record.kind === "project" && record.facts.type === "project")
      .flatMap((record) => (record.facts.type === "project" ? record.facts.technologies : []))
      .map(normalizeText)
      .filter((technology) => includesPhrase(query, technology)),
  );

  return new Set(
    [...matches].filter(
      (technology) => ![...matches].some((other) => other !== technology && includesPhrase(other, technology)),
    ),
  );
}

function matchesRequestedTechnologies(record: EvidenceRecord, technologies: Set<string>): boolean {
  if (technologies.size === 0) return true;
  if (record.kind !== "project" || record.facts.type !== "project") return false;
  const recordTechnologies = new Set(record.facts.technologies.map(normalizeText));
  return [...technologies].every((technology) => recordTechnologies.has(technology));
}

function scoreEvidence(query: string, queryTokens: Set<string>, record: EvidenceRecord): number {
  let score = 0;
  if (record.kind === "project" && (queryTokens.has("project") || queryTokens.has("projects"))) score += 20;
  if (includesPhrase(query, record.title)) score += 12;
  if (includesPhrase(query, record.searchText)) score += 10;
  for (const alias of record.aliases) if (includesPhrase(query, alias)) score += 10;

  const titleTokens = new Set(tokenize(record.title));
  const aliasTokens = new Set(record.aliases.flatMap(tokenize));
  const searchTokens = new Set(tokenize(record.searchText));

  for (const token of queryTokens) {
    if (titleTokens.has(token)) score += 5;
    else if (aliasTokens.has(token)) score += 4;
    else if (searchTokens.has(token)) score += 2;
  }
  return score;
}

export function retrieveEvidence(question: string): EvidenceRecord[] {
  const query = normalizeText(question);
  const queryTokens = new Set(tokenize(question));
  if (queryTokens.size === 0) return [];
  const hasProjectIntent = queryTokens.has("project") || queryTokens.has("projects");
  const technologies = requestedTechnologies(query);

  return evidenceRegistry
    .filter((record) => !hasProjectIntent || record.kind === "project")
    .filter((record) => !hasProjectIntent || matchesRequestedTechnologies(record, technologies))
    .map((record) => ({ record, score: scoreEvidence(query, queryTokens, record) }))
    .filter(({ score }) => score >= MIN_SCORE)
    .sort((left, right) => right.score - left.score || (left.record.id < right.record.id ? -1 : left.record.id > right.record.id ? 1 : 0))
    .slice(0, MAX_MATCHES)
    .map(({ record }) => record);
}
