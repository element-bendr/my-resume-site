import { describe, expect, it } from "vitest";
import worker from "../worker/index";

describe("portfolio Worker API", () => {
  it("returns a no-store health response", async () => {
    const response = await worker.fetch(new Request("https://portfolio.example/api/health"));
    expect(response.status).toBe(200);
    expect(response.headers.get("cache-control")).toBe("no-store");
    await expect(response.json()).resolves.toEqual({
      ok: true,
      service: "vijay-kumaran-portfolio-world",
      stage: "app-foundation",
    });
  });

  it("returns structured 404s for unknown API routes", async () => {
    const response = await worker.fetch(new Request("https://portfolio.example/api/nope"));
    expect(response.status).toBe(404);
    await expect(response.json()).resolves.toEqual({
      ok: false,
      error: "not_found",
    });
  });

  it("returns grounded evidence through POST /api/ask with no-store security headers", async () => {
    const response = await worker.fetch(new Request("https://portfolio.example/api/ask", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question: "What technologies does PCAS use?" }),
    }));

    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toContain("application/json");
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(response.headers.get("x-content-type-options")).toBe("nosniff");
    expect(response.headers.get("referrer-policy")).toBe("no-referrer");
    expect(response.headers.get("access-control-allow-origin")).toBeNull();
    const body = await response.json();
    expect(body).toMatchObject({ ok: true, support: "grounded" });
    expect(body.matches.length).toBeGreaterThan(0);
  });

  it("preserves unsupported questions as a successful insufficient-evidence result", async () => {
    const response = await worker.fetch(askRequest({ question: "What was Vijay's salary?" }));
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toMatchObject({
      ok: true,
      support: "insufficient_evidence",
      matches: [],
    });
  });

  it("rejects unsupported methods with Allow: POST", async () => {
    const response = await worker.fetch(new Request("https://portfolio.example/api/ask"));
    expect(response.status).toBe(405);
    expect(response.headers.get("allow")).toBe("POST");
    await expect(response.json()).resolves.toMatchObject({
      support: "invalid_request",
      error: { code: "method_not_allowed" },
    });
  });

  it("rejects non-JSON content types", async () => {
    const response = await worker.fetch(new Request("https://portfolio.example/api/ask", {
      method: "POST",
      headers: { "content-type": "text/plain" },
      body: "question",
    }));
    expect(response.status).toBe(415);
    await expect(response.json()).resolves.toMatchObject({ error: { code: "unsupported_media_type" } });
  });

  it.each(["", "not-json", "{\"question\":" ])("rejects malformed JSON without echoing input", async (body) => {
    const response = await worker.fetch(askRequest(body));
    expect(response.status).toBe(400);
    const responseBody = await response.text();
    if (body) expect(responseBody).not.toContain(body);
    expect(JSON.parse(responseBody)).toEqual({
      ok: false,
      answer: "",
      matches: [],
      support: "invalid_request",
      error: {
        code: "invalid_json",
        message: "The request body must be valid JSON.",
      },
    });
  });

  it.each([
    JSON.stringify({ question: "  \t\n " }),
    JSON.stringify({ question: "question", extra: "field" }),
    JSON.stringify(["question"]),
    JSON.stringify({ question: 42 }),
  ])("rejects structurally invalid or empty questions", async (body) => {
    const response = await worker.fetch(askRequest(body));
    expect(response.status).toBe(400);
    await expect(response.json()).resolves.toMatchObject({ error: { code: "invalid_request" } });
  });

  it("counts normalized question limits in Unicode code points and does not truncate", async () => {
    const valid = await worker.fetch(askRequest({ question: `${"😀".repeat(500)}` }));
    expect(valid.status).toBe(200);
    const tooLongQuestion = "😀".repeat(501);
    const tooLong = await worker.fetch(askRequest({ question: tooLongQuestion }));
    expect(tooLong.status).toBe(400);
    const body = await tooLong.text();
    expect(body).not.toContain(tooLongQuestion);
    expect(JSON.parse(body)).toMatchObject({ error: { code: "question_too_long" } });
  });

  it("rejects request bodies beyond 4096 bytes", async () => {
    const exactlyAtLimit = `{"question":"${"x".repeat(4081)}"}`;
    expect(new TextEncoder().encode(exactlyAtLimit)).toHaveLength(4096);
    const boundaryResponse = await worker.fetch(askRequest(exactlyAtLimit));
    expect(boundaryResponse.status).toBe(400);
    await expect(boundaryResponse.json()).resolves.toMatchObject({ error: { code: "question_too_long" } });

    const response = await worker.fetch(askRequest({ question: "x".repeat(4100) }));
    expect(response.status).toBe(413);
    await expect(response.json()).resolves.toMatchObject({ error: { code: "payload_too_large" } });
  });
});

function askRequest(payload: unknown): Request {
  return new Request("https://portfolio.example/api/ask", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: typeof payload === "string" ? payload : JSON.stringify(payload),
  });
}
