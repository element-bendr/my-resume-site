import { retrieveEvidence } from "./retrieve";
import type { AskResponse, EvidenceMatch } from "./types";
import type { EvidenceRecord } from "./evidence";

export const INSUFFICIENT_EVIDENCE_ANSWER = "I don't have verified portfolio evidence to answer that.";

function matchFor(record: EvidenceRecord): EvidenceMatch {
  return { kind: record.kind, id: record.id, title: record.title, sourceRefs: [...record.sourceRefs] };
}

function sentenceFor(record: EvidenceRecord): string {
  switch (record.facts.type) {
    case "identity":
      return `${record.facts.summary} Consulting positioning: ${record.facts.consultingTitle}. Engineering positioning: ${record.facts.engineeringPositioning}.`;
    case "project": {
      const technologies = record.facts.technologies.length
        ? ` Technologies include ${record.facts.technologies.join(", ")}.`
        : "";
      return `${record.title}: ${record.facts.summary}${technologies}`;
    }
    case "experience":
      return `${record.facts.role} at ${record.facts.organization} (${record.facts.period}). ${record.facts.summary}`;
    case "skill":
      return `${record.title} is listed under ${record.facts.category}.`;
    case "hobby":
      return `${record.title} is listed as a hobby.`;
    case "link":
      return `${record.title}: ${record.facts.href}`;
  }
}

export function answerQuestion(question: string): AskResponse {
  const records = retrieveEvidence(question);
  if (records.length === 0) {
    return {
      ok: true,
      answer: INSUFFICIENT_EVIDENCE_ANSWER,
      matches: [],
      support: "insufficient_evidence",
    };
  }

  return {
    ok: true,
    answer: records.slice(0, 3).map(sentenceFor).join(" "),
    matches: records.map(matchFor),
    support: "grounded",
  };
}
