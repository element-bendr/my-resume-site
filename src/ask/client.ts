import { ASK_MAX_QUESTION_CODE_POINTS } from "./types";
import type { AskErrorCode, AskErrorResponse, AskResponse } from "./types";

export class AskClientError extends Error {
  constructor(
    message: string,
    readonly code?: AskErrorCode,
    readonly status?: number,
  ) {
    super(message);
    this.name = "AskClientError";
  }
}

export interface AskClientOptions {
  signal?: AbortSignal;
  fetcher?: typeof fetch;
}

function normalizeQuestion(question: string): string {
  return question.replace(/\p{White_Space}+/gu, " ").trim();
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isAskResponse(value: unknown): value is AskResponse {
  if (!isRecord(value) || value.ok !== true || typeof value.answer !== "string" || !Array.isArray(value.matches)) {
    return false;
  }
  if (value.support !== "grounded" && value.support !== "insufficient_evidence") return false;

  const kinds = new Set(["identity", "project", "experience", "skill", "hobby", "link"]);
  const matchesAreValid = value.matches.every((match: unknown) =>
    isRecord(match) &&
    typeof match.kind === "string" && kinds.has(match.kind) &&
    typeof match.id === "string" && typeof match.title === "string" &&
    Array.isArray(match.sourceRefs) && match.sourceRefs.every((sourceRef: unknown) => typeof sourceRef === "string"),
  );
  if (!matchesAreValid) return false;
  return value.support === "grounded" ? value.matches.length > 0 : value.matches.length === 0;
}

function isAskErrorResponse(value: unknown): value is AskErrorResponse {
  if (!isRecord(value) || value.ok !== false || value.answer !== "" || !Array.isArray(value.matches) || value.matches.length !== 0) {
    return false;
  }
  if (value.support !== "invalid_request" || !isRecord(value.error)) return false;
  const codes = new Set<AskErrorCode>([
    "method_not_allowed",
    "unsupported_media_type",
    "invalid_json",
    "invalid_request",
    "question_too_long",
    "payload_too_large",
    "internal_error",
  ]);
  return typeof value.error.code === "string" && codes.has(value.error.code as AskErrorCode) &&
    typeof value.error.message === "string";
}

export async function postAskQuestion(question: string, options: AskClientOptions = {}): Promise<AskResponse> {
  const normalizedQuestion = normalizeQuestion(question);
  if (!normalizedQuestion) {
    throw new AskClientError("Enter a question before asking.", "invalid_request");
  }
  if ([...normalizedQuestion].length > ASK_MAX_QUESTION_CODE_POINTS) {
    throw new AskClientError(
      `Keep the question to ${ASK_MAX_QUESTION_CODE_POINTS} Unicode code points or fewer.`,
      "question_too_long",
    );
  }

  let response: Response;
  try {
    response = await (options.fetcher ?? fetch)("/api/ask", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question: normalizedQuestion }),
      signal: options.signal,
    });
  } catch (error) {
    if (options.signal?.aborted) throw error;
    throw new AskClientError("Could not reach Ask. Check your connection and try again.");
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch (error) {
    if (options.signal?.aborted) throw error;
    throw new AskClientError("Ask returned an unreadable response.", undefined, response.status);
  }

  if (!response.ok) {
    if (isAskErrorResponse(body)) {
      throw new AskClientError(body.error.message, body.error.code, response.status);
    }
    throw new AskClientError("Ask could not complete the request. Try again.", undefined, response.status);
  }
  if (!isAskResponse(body)) {
    throw new AskClientError("Ask returned an unexpected response.", undefined, response.status);
  }
  return body;
}
