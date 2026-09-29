export type EvidenceKind = "identity" | "project" | "experience" | "skill" | "hobby" | "link";

export interface EvidenceMatch {
  kind: EvidenceKind;
  id: string;
  title: string;
  sourceRefs: string[];
}

export interface AskResponse {
  ok: true;
  answer: string;
  matches: EvidenceMatch[];
  support: "grounded" | "insufficient_evidence";
}
