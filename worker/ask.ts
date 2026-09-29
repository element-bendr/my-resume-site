import { answerQuestion } from "../src/ask/answer";
import { ASK_MAX_QUESTION_CODE_POINTS, ASK_MAX_REQUEST_BYTES } from "../src/ask/types";
import type { AskErrorCode, AskErrorResponse, AskResponse } from "../src/ask/types";

const messages: Record<AskErrorCode, string> = {
  method_not_allowed: "Use POST to submit a question.",
  unsupported_media_type: "Send the question as JSON.",
  invalid_json: "The request body must be valid JSON.",
  invalid_request: "The request must contain only a non-empty question string.",
  question_too_long: "The question exceeds the 500 Unicode code point limit.",
  payload_too_large: "The request body exceeds the 4096 byte limit.",
  internal_error: "The Ask service could not complete the request.",
};

function json(body: AskResponse | AskErrorResponse, status = 200, extraHeaders?: HeadersInit): Response {
  const headers = new Headers(extraHeaders);
  headers.set("content-type", "application/json; charset=utf-8");
  headers.set("cache-control", "no-store");
  headers.set("x-content-type-options", "nosniff");
  headers.set("referrer-policy", "no-referrer");
  return new Response(JSON.stringify(body), { status, headers });
}

function failure(code: AskErrorCode, status: number, headers?: HeadersInit): Response {
  return json(
    {
      ok: false,
      answer: "",
      matches: [],
      support: "invalid_request",
      error: { code, message: messages[code] },
    },
    status,
    headers,
  );
}

async function readBoundedBody(request: Request): Promise<Uint8Array | null> {
  const contentLength = request.headers.get("content-length");
  if (contentLength !== null && Number(contentLength) > ASK_MAX_REQUEST_BYTES) {
    await request.body?.cancel();
    return null;
  }

  if (!request.body) return new Uint8Array();

  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > ASK_MAX_REQUEST_BYTES) {
      await reader.cancel();
      return null;
    }
    chunks.push(value);
  }

  const body = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return body;
}

function normalizeQuestion(question: string): string {
  return question.replace(/\p{White_Space}+/gu, " ").trim();
}

export async function handleAskRequest(request: Request): Promise<Response> {
  if (request.method !== "POST") {
    return failure("method_not_allowed", 405, { allow: "POST" });
  }

  const mediaType = request.headers.get("content-type")?.split(";", 1)[0].trim().toLowerCase();
  if (mediaType !== "application/json") {
    return failure("unsupported_media_type", 415);
  }

  try {
    const body = await readBoundedBody(request);
    if (body === null) return failure("payload_too_large", 413);

    let payload: unknown;
    try {
      payload = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(body));
    } catch {
      return failure("invalid_json", 400);
    }

    if (
      payload === null ||
      typeof payload !== "object" ||
      Array.isArray(payload) ||
      Object.keys(payload).length !== 1 ||
      !Object.hasOwn(payload, "question") ||
      typeof (payload as { question?: unknown }).question !== "string"
    ) {
      return failure("invalid_request", 400);
    }

    const question = normalizeQuestion((payload as { question: string }).question);
    if (!question) return failure("invalid_request", 400);
    if ([...question].length > ASK_MAX_QUESTION_CODE_POINTS) {
      return failure("question_too_long", 400);
    }

    return json(answerQuestion(question));
  } catch {
    return failure("internal_error", 500);
  }
}
