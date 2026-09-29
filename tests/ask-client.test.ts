import { describe, expect, it, vi } from "vitest";
import { postAskQuestion } from "../src/ask/client";
import { ASK_MAX_QUESTION_CODE_POINTS } from "../src/ask/types";

const grounded = {
  ok: true,
  answer: "PCAS (Production-oriented career acquisition system): evidence-backed answer.",
  matches: [{ kind: "project", id: "pcas", title: "Personal Career Acquisition System", sourceRefs: ["public-engineering-profile"] }],
  support: "grounded",
} as const;

describe("Ask API client", () => {
  it("posts the normalized question and returns the answer unchanged", async () => {
    const fetcher = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) =>
      Response.json(grounded),
    );
    const result = await postAskQuestion("  What is PCAS?\n ", { fetcher });

    expect(fetcher).toHaveBeenCalledWith("/api/ask", expect.objectContaining({
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question: "What is PCAS?" }),
    }));
    expect(result).toEqual(grounded);
  });

  it("uses the exact shared server question limit and blocks overlong input locally", async () => {
    expect(ASK_MAX_QUESTION_CODE_POINTS).toBe(500);
    const fetcher = vi.fn(async () => Response.json(grounded));
    await expect(postAskQuestion("😀".repeat(ASK_MAX_QUESTION_CODE_POINTS + 1), { fetcher }))
      .rejects.toMatchObject({ name: "AskClientError", code: "question_too_long" });
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("rejects whitespace-only input without making a request", async () => {
    const fetcher = vi.fn(async () => Response.json(grounded));
    await expect(postAskQuestion(" \t\n ", { fetcher }))
      .rejects.toMatchObject({ code: "invalid_request" });
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("surfaces the server's stable non-echoing validation message", async () => {
    const fetcher = async () => Response.json({
      ok: false,
      answer: "",
      matches: [],
      support: "invalid_request",
      error: { code: "question_too_long", message: "The question exceeds the 500 Unicode code point limit." },
    }, { status: 400 });

    await expect(postAskQuestion("What happened?", { fetcher }))
      .rejects.toMatchObject({
        name: "AskClientError",
        code: "question_too_long",
        status: 400,
        message: "The question exceeds the 500 Unicode code point limit.",
      });
  });

  it("uses generic errors for network and malformed success responses", async () => {
    await expect(postAskQuestion("What happened?", { fetcher: async () => { throw new Error("private detail"); } }))
      .rejects.toMatchObject({ message: "Could not reach Ask. Check your connection and try again." });
    await expect(postAskQuestion("What happened?", { fetcher: async () => Response.json({ answer: "not a contract" }) }))
      .rejects.toMatchObject({ message: "Ask returned an unexpected response." });
  });

  it("preserves aborts so the page can discard stale or unmounted requests", async () => {
    const controller = new AbortController();
    const abort = new DOMException("Aborted", "AbortError");
    const fetcher = async () => {
      controller.abort();
      throw abort;
    };
    await expect(postAskQuestion("What happened?", { signal: controller.signal, fetcher }))
      .rejects.toBe(abort);
  });
});
