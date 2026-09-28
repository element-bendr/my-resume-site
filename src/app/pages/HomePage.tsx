import { Link } from "react-router";
import { featuredProjects, identity } from "../../content";

export function HomePage() {
  return (
    <>
      <section className="hero section">
        <p className="eyebrow">{identity.consultingTitle}</p>
        <h1>{identity.tagline}</h1>
        <p className="hero-summary">{identity.summary}</p>
        <p className="engineering-line">{identity.engineeringPositioning}</p>

        <div className="action-row" aria-label="Primary actions">
          <Link className="button button-primary" to="/play">
            Enter world
          </Link>
          <Link className="button button-secondary" to="/projects">
            View projects
          </Link>
          <Link className="button button-quiet" to="/resume">
            Read resume
          </Link>
        </div>
      </section>

      <section className="section" aria-labelledby="build-heading">
        <div className="section-heading">
          <p className="eyebrow">What I build</p>
          <h2 id="build-heading">Websites. Business systems. AI automations.</h2>
        </div>
        <div className="feature-grid">
          <article className="panel">
            <span className="panel-index">01</span>
            <h3>Websites</h3>
            <p>Fast, maintainable web systems focused on clarity, delivery, and business use.</p>
          </article>
          <article className="panel">
            <span className="panel-index">02</span>
            <h3>Business systems</h3>
            <p>Admin tools and workflows that make repeated operational work easier to run.</p>
          </article>
          <article className="panel">
            <span className="panel-index">03</span>
            <h3>AI automations</h3>
            <p>Governed AI-assisted workflows with explicit state, evidence, and human review.</p>
          </article>
        </div>
      </section>

      <section className="section" aria-labelledby="selected-heading">
        <div className="section-heading section-heading-row">
          <div>
            <p className="eyebrow">Selected work</p>
            <h2 id="selected-heading">Systems with evidence behind them.</h2>
          </div>
          <Link className="text-link" to="/projects">
            All projects
          </Link>
        </div>
        <div className="project-grid">
          {featuredProjects.map((project) => (
            <article className="project-card" key={project.id}>
              <p className="project-status">{project.status}</p>
              <h3>{project.title}</h3>
              <p>{project.shortSummary}</p>
              <div className="tag-row" aria-label="Technologies">
                {project.technologies.slice(0, 4).map((technology) => (
                  <span className="tag" key={technology}>
                    {technology}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
