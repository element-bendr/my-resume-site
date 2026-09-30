import { lazy, Suspense } from "react";
import { Link } from "react-router";

const WorldEntry = lazy(() => import("../../world/WorldEntry"));

export function PlayPage() {
  return (
    <section className="world-route" aria-labelledby="play-heading">
      <h1 id="play-heading" className="sr-only">
        Interactive Command Center
      </h1>
      <Suspense
        fallback={
          <div className="world-loading" role="status">
            Initializing Command Center…
          </div>
        }
      >
        <WorldEntry />
      </Suspense>
      <div className="world-direct-fallback">
        <span>Prefer the conventional portfolio?</span>
        <Link to="/projects">Projects</Link>
        <Link to="/resume">Resume</Link>
        <Link to="/contact">Contact</Link>
      </div>
    </section>
  );
}
