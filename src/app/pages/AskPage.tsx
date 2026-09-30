import { useEffect, useRef, useState, type FormEvent } from "react";
import { AskClientError, postAskQuestion } from "../../ask/client";
import { publicSourceLabels } from "../../ask/public-source-labels";
import { ASK_MAX_QUESTION_CODE_POINTS, type AskResponse, type EvidenceMatch } from "../../ask/types";

const examples = [
  "Which projects use Cloudflare Workers?",
  "What was Vijay's role at HCL Comnet?",
  "Does Vijay use TypeScript?",
  "What about anime?",
];

function sourceLabelsFor(match: EvidenceMatch): string[] {
  const labels = match.sourceRefs.map((sourceRef) => publicSourceLabels[sourceRef] ?? "Verified portfolio evidence");
  return [...new Set(labels)];
}

function normalizedCodePointCount(value: string): number {
  const normalized = value.replace(/\p{White_Space}+/gu, " ").trim();
  return [...normalized].length;
}

export function AskPage() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const controllerRef = useRef<AbortController | null>(null);

  useEffect(() => () => controllerRef.current?.abort(), []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setResponse(null);
    setError("");
    setLoading(true);

    try {
      const result = await postAskQuestion(question, { signal: controller.signal });
      if (!controller.signal.aborted) setResponse(result);
    } catch (cause) {
      if (controller.signal.aborted) return;
      setError(cause instanceof AskClientError
        ? cause.message
        : "Ask could not complete the request. Try again.");
    } finally {
      if (controllerRef.current === controller) {
        controllerRef.current = null;
        if (!controller.signal.aborted) setLoading(false);
      }
    }
  }

  return (
    <section className="section page-section ask-page" aria-labelledby="ask-heading">
      <div className="section-heading ask-heading">
        <p className="eyebrow">Grounded Q&amp;A</p>
        <h1 id="ask-heading">Ask about the work.</h1>
        <p>
          Get a concise answer from verified portfolio evidence. When the evidence is not there,
          Ask will say so.
        </p>
      </div>

      <div className="ask-layout">
        <form className="panel ask-form" onSubmit={handleSubmit}>
          <label className="ask-label" htmlFor="ask-question">Your question</label>
          <textarea
            id="ask-question"
            name="question"
            rows={4}
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="For example, which projects use Cloudflare Workers?"
            aria-describedby={error
              ? "ask-question-hint ask-question-count ask-error-message"
              : "ask-question-hint ask-question-count"}
            aria-invalid={Boolean(error)}
            disabled={loading}
            required
          />
          <div className="ask-form-meta">
            <p id="ask-question-hint">Up to {ASK_MAX_QUESTION_CODE_POINTS} Unicode code points. Questions are not saved.</p>
            <span id="ask-question-count" className="ask-count">
              {normalizedCodePointCount(question)} / {ASK_MAX_QUESTION_CODE_POINTS}
            </span>
          </div>
          <button className="button button-primary ask-submit" type="submit" disabled={loading}>
            {loading ? "Checking evidence…" : "Ask"}
          </button>
        </form>

        <aside className="panel ask-examples" aria-labelledby="ask-examples-heading">
          <p className="panel-index">Try a question</p>
          <h2 id="ask-examples-heading">Start with the evidence</h2>
          <ul>
            {examples.map((example) => (
              <li key={example}>
                <button
                  className="ask-example"
                  type="button"
                  onClick={() => setQuestion(example)}
                  disabled={loading}
                >
                  {example}
                </button>
              </li>
            ))}
          </ul>
        </aside>
      </div>

      <div
        className="ask-response"
        aria-live="polite"
        aria-atomic="false"
        aria-busy={loading}
      >
        {loading ? <p className="ask-status" role="status">Looking for verified evidence…</p> : null}
        {error ? (
          <div id="ask-error-message" className="panel ask-error" role="alert">
            <h2>Could not answer yet</h2>
            <p>{error}</p>
          </div>
        ) : null}
        {response ? (
          <section className="panel ask-result" aria-labelledby="ask-result-heading">
            <p className="panel-index">
              {response.support === "grounded" ? "Grounded answer" : "No matching evidence"}
            </p>
            <h2 id="ask-result-heading">{response.support === "grounded" ? "Here’s what the portfolio supports" : "Not verified in this portfolio"}</h2>
            <p className="ask-answer-text">{response.answer}</p>
            {response.matches.length > 0 ? (
              <div className="ask-evidence">
                <h3>Matched evidence</h3>
                <ul className="ask-match-list">
                  {response.matches.map((match) => {
                    const labels = sourceLabelsFor(match);
                    return (
                      <li className="ask-match" key={`${match.kind}:${match.id}`}>
                        <span className="ask-match-kind">{match.kind}</span>
                        <strong>{match.title}</strong>
                        {labels.length > 0 ? (
                          <p>Sources: {labels.join(", ")}</p>
                        ) : null}
                      </li>
                    );
                  })}
                </ul>
              </div>
            ) : null}
          </section>
        ) : null}
      </div>
    </section>
  );
}
