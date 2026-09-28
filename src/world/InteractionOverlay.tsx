import { useEffect, useRef } from "react";
import { Link } from "react-router";
import { projects } from "../content";
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
              {station.kind === "ask" ? "Ask Terminal" : "Project evidence"}
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
        ) : (
          <>
            <p>
              The grounded Ask backend arrives in Stage 05. The conventional Ask route already
              preserves the direct, non-3D path to project evidence.
            </p>
            <div className="action-row">
              <Link className="button button-primary" to="/ask" onClick={onClose}>
                Open Ask
              </Link>
              <Link className="button button-secondary" to="/projects" onClick={onClose}>
                Browse evidence
              </Link>
            </div>
          </>
        )}
      </section>
    </div>
  );
}
