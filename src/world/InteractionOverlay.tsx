import { useEffect, useRef } from "react";
import { Link } from "react-router";
import { experience, hobbies, projects } from "../content";
import type { StationConfig } from "./world-config";

interface InteractionOverlayProps {
  station: StationConfig;
  onClose: () => void;
}

export function InteractionOverlay({ station, onClose }: InteractionOverlayProps) {
  const closeButton = useRef<HTMLButtonElement>(null);
  const project = station.projectId
    ? projects.find((item) => item.id === station.projectId)
    : undefined;
  const experienceEntry = station.experienceId
    ? experience.find((item) => item.id === station.experienceId)
    : undefined;
  const hobby = station.hobbyId
    ? hobbies.find((item) => item.id === station.hobbyId)
    : undefined;

  useEffect(() => {
    closeButton.current?.focus();
  }, [station.id]);

  return (
    <div
      className="world-overlay-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <section
        className="world-interaction-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="world-interaction-title"
      >
        <div className="world-panel-heading">
          <div>
            <span className="world-hud-kicker">
              {station.kind === "ask"
                ? "Ask Terminal"
                : station.kind === "experience"
                  ? "Timeline"
                  : station.kind === "hobby"
                    ? "Hobby District"
                    : "Project evidence"}
            </span>
            <h2 id="world-interaction-title">{station.title}</h2>
          </div>
          <button
            ref={closeButton}
            type="button"
            className="world-close"
            onClick={onClose}
            aria-label="Close interaction"
          >
            ×
          </button>
        </div>

        {project ? (
          <>
            <p className="project-status">{project.status}</p>
            <p>{project.shortSummary}</p>
            <div className="tag-row" aria-label="Project technologies">
              {project.technologies.map((technology) => (
                <span className="tag" key={technology}>
                  {technology}
                </span>
              ))}
            </div>
            <div className="link-row">
              {project.publicLinks.map((link) => (
                <a href={link.url} target="_blank" rel="noreferrer" key={link.url}>
                  {link.label}
                </a>
              ))}
              <Link to="/projects" onClick={onClose}>
                All projects
              </Link>
            </div>
          </>
        ) : experienceEntry ? (
          <>
            <p className="project-status">{experienceEntry.period}</p>
            <p>{experienceEntry.role} · {experienceEntry.organization}</p>
            <p>{experienceEntry.summary}</p>
            <ul>
              {experienceEntry.highlights.map((highlight) => (
                <li key={highlight}>{highlight}</li>
              ))}
            </ul>
            <div className="link-row">
              <Link to="/resume" onClick={onClose}>Full resume</Link>
            </div>
          </>
        ) : hobby ? (
          <>
            <p>{hobby.worldMotif}</p>
            <p>
              This district is intentionally personal rather than a professional scorecard. No
              invented rankings, achievements, or biographical claims are attached to it.
            </p>
          </>
        ) : station.kind === "ask" ? (
          <>
            <p>
              Ask about verified portfolio evidence from the projects, experience, and skills shown
              across this portfolio.
            </p>
            <div className="action-row">
              <Link className="button button-primary" to="/ask" onClick={onClose}>
                Open Ask
              </Link>
            </div>
          </>
        ) : (
          <>
            <p>
              Additional details are not available for this station.
            </p>
            <div className="action-row">
              <Link className="button button-secondary" to="/projects" onClick={onClose}>
                Browse projects
              </Link>
            </div>
          </>
        )}
      </section>
    </div>
  );
}
