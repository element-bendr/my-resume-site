import { Link } from "react-router";
import { hobbies } from "../../content";

export function PlayPage() {
  return (
    <section className="section page-section" aria-labelledby="play-heading">
      <div className="world-placeholder">
        <p className="eyebrow">World mode · foundation gate</p>
        <h1 id="play-heading">The world entrance is reserved.</h1>
        <p>
          The production 3D Command Center is built in the next stage. This route already exists so
          navigation, Cloudflare SPA fallback, accessibility, and non-WebGL escape paths can be
          certified before the renderer arrives.
        </p>
        <div className="world-map-preview" aria-label="Planned portfolio world districts">
          <span>Timeline</span>
          <span>Client Street</span>
          <strong>Command Center</strong>
          <span>Hobby District</span>
          <span>Build Lab</span>
          <span>Automation Lab</span>
          <span>Ask Terminal</span>
        </div>
        <div className="action-row">
          <Link className="button button-secondary" to="/projects">
            Explore projects normally
          </Link>
          <Link className="button button-quiet" to="/resume">
            Open resume
          </Link>
        </div>
      </div>

      <section className="section inset-section" aria-labelledby="hobbies-heading">
        <p className="eyebrow">Hobby District</p>
        <h2 id="hobbies-heading">Personal themes already approved for the world.</h2>
        <div className="feature-grid">
          {hobbies.map((hobby) => (
            <article className="panel" key={hobby.id}>
              <h3>{hobby.label}</h3>
              <p>{hobby.worldMotif}</p>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
