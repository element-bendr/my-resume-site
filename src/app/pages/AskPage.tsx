import { Link } from "react-router";

export function AskPage() {
  return (
    <section className="section page-section narrow-page" aria-labelledby="ask-heading">
      <p className="eyebrow">Grounded Q&amp;A</p>
      <h1 id="ask-heading">Ask about the work.</h1>
      <p>
        The evidence-grounded Ask backend is integrated in Stage 05. Until then, the conventional
        portfolio exposes the same project and resume evidence directly instead of pretending a
        disconnected text box is useful.
      </p>
      <div className="action-row">
        <Link className="button button-primary" to="/projects">
          Browse project evidence
        </Link>
        <Link className="button button-secondary" to="/resume">
          Read resume
        </Link>
      </div>
    </section>
  );
}
