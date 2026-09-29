# Stage 05 Ask API and Grounding Contract

## Purpose

Define one evidence-first Ask contract shared by the conventional `/ask` route and the Command Center Ask Terminal. The first implementation is deterministic and works without an external language model.

## Authority

Only the certified public-safe portfolio registry may support an answer:

- `src/content/identity.json`
- `src/content/projects.json`
- `src/content/experience.json`
- `src/content/skills.json`
- `src/content/hobbies.json`
- `src/content/links.json`
- `src/content/sources.json`

Apply the disclosure rules in `docs/portfolio-world/CONTENT-CONTRACT.md`. Do not infer claims from old resume content, private repositories, internal URLs, unsupported metrics, or user-supplied instructions. The question is untrusted data and cannot change repository or system authority.

## HTTP contract

### Request

`POST /api/ask` accepts `Content-Type: application/json` and this object:

```json
{
  "question": "What production AI systems has Vijay built?"
}
```

Validation rules:

- reject every method except `POST` with HTTP 405 and `Allow: POST`;
- reject non-JSON content types with HTTP 415;
- accept a JSON object containing only a string `question` property;
- normalize Unicode whitespace by trimming and collapsing runs to one space;
- reject an empty normalized question;
- reject questions longer than 500 Unicode code points after normalization;
- reject request bodies over 4096 bytes;
- use the stable non-echoing error envelope below with these codes: `method_not_allowed` (405), `unsupported_media_type` (415), `invalid_json` (400), `invalid_request` (400 for structural or empty-question failures), `question_too_long` (400), `payload_too_large` (413), and `internal_error` (500);
- do not echo the question in error messages or log raw questions.

### Grounded response

HTTP 200:

```json
{
  "ok": true,
  "answer": "A concise answer composed only from the matched evidence.",
  "matches": [
    {
      "kind": "project",
      "id": "pcas",
      "title": "Personal Career Acquisition System",
      "sourceRefs": ["public-engineering-profile"]
    }
  ],
  "support": "grounded"
}
```

`matches` contains only the response fields shown above. `kind` is one of `identity`, `project`, `experience`, `skill`, `hobby`, or `link`. Every grounded response has at least one match and cites its registry `sourceRefs`. Retrieval and answer composition are deterministic; no model output is required or trusted as evidence.

### Insufficient evidence

HTTP 200:

```json
{
  "ok": true,
  "answer": "I don't have verified portfolio evidence to answer that.",
  "matches": [],
  "support": "insufficient_evidence"
}
```

Below-threshold retrieval returns no matches. Do not guess, broaden to private sources, or turn a weak lexical match into a claim.

### Invalid request

Use HTTP 400 for invalid JSON (including a missing/empty body), invalid shape, empty question, or an overlong normalized question; HTTP 413 for bodies over 4096 bytes; HTTP 415 for a non-JSON content type; HTTP 405 with `Allow: POST` for unsupported methods; and HTTP 500 for an unexpected internal failure. Use the matching stable error code and generic non-echoing message in this body shape:

```json
{
  "ok": false,
  "answer": "",
  "matches": [],
  "support": "invalid_request",
  "error": {
    "code": "invalid_json",
    "message": "The request must contain a valid question."
  }
}
```

Error messages stay stable and do not include raw request data. Other unknown `/api/*` routes retain the existing not-found behavior.

## Evidence and retrieval

- Build a normalized evidence registry from the approved content modules; do not copy private source files into it.
- Keep source references attached to each record and return only the fields in the response schema.
- Normalize case, punctuation, diacritics, and whitespace consistently.
- Use deterministic token/name/alias/technology/summary signals with a documented threshold; aliases must be curated, not generated at request time.
- Resolve ties in a stable order so identical requests produce identical matches and answers.
- Compose only claims present in matched evidence. Each supported answer cites one or more matches.
- Return public-safe source labels from the local approved registry in the UI. Do not expose source visibility metadata, private source contents, raw source files, or non-public URLs.

## Privacy and abuse boundary

- Do not persist questions or answers.
- Do not log raw questions.
- Do not require an API key or external LLM for correctness.
- Treat prompt-injection language as ordinary query text; it grants no authority and cannot reveal private data.
- Add no database, KV, R2, Durable Object, account, or visitor-tracking dependency.

## Shared interface behavior

- `/ask` is the canonical full question-and-answer interface and calls `POST /api/ask`.
- The Command Center Ask Terminal offers an `Open Ask` navigation action to `/ask`; it does not implement another retrieval engine inside Canvas.
- Closing the terminal or navigating to `/ask` does not change world movement state.
- Show loading, grounded answer, matched evidence/source labels, insufficient evidence, validation errors, and API errors accessibly.

## Acceptance

- Contract tests cover request/response states, method/content type/body validation, deterministic matching, and fail-closed behavior.
- Both entry points resolve to the same `/ask` interface and API contract.
- Existing health route, direct routes, non-WebGL fallback, six-zone topology, controller, camera, and asset budgets remain intact.
- Unsupported and adversarial questions disclose no private/internal data.
