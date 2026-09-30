import { projects } from "../../content";

export function ProjectsPage() {
  return (
    <section className="section page-section" aria-labelledby="projects-heading">
      <div className="section-heading">
        <p className="eyebrow">Evidence-backed work</p>
        <h1 id="projects-heading">Projects</h1>
        <p>
          Public descriptions stay within the proof and disclosure boundaries recorded in the
          portfolio content contract.
        </p>
      </div>

      <div className="project-grid">
        {projects.map((project) => (
          <article className="project-card" key={project.id}>
            <div className="card-meta">
              <span>{project.worldZone.replaceAll("-", " ")}</span>
              {project.featured ? <span>Featured</span> : null}
            </div>
            <h2>{project.title}</h2>
            <p className="project-status">{project.status}</p>
            <p>{project.shortSummary}</p>
            <div className="tag-row" aria-label={`${project.title} technologies`}>
              {project.technologies.map((technology) => (
                <span className="tag" key={technology}>
                  {technology}
                </span>
              ))}
            </div>
            {project.publicLinks.length > 0 ? (
              <div className="link-row">
                {project.publicLinks.map((link) => (
                  <a key={link.url} href={link.url} rel="noreferrer" target="_blank">
                    {link.label}
                  </a>
                ))}
              </div>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
