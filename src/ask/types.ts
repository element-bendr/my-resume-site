export type EvidenceKind = "identity" | "project" | "experience" | "skill" | "hobby" | "link";

export const ASK_MAX_QUESTION_CODE_POINTS = 500;
export const ASK_MAX_REQUEST_BYTES = 4096;

export type AskErrorCode =
  | "method_not_allowed"
  | "unsupported_media_type"
  | "invalid_json"
  | "invalid_request"
  | "question_too_long"
  | "payload_too_large"
  | "internal_error";

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

export interface AskErrorResponse {
  ok: false;
  answer: "";
  matches: [];
  support: "invalid_request";
  error: { code: AskErrorCode; message: string };
}
