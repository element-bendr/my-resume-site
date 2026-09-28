import { Link } from "react-router";
import type { StationConfig } from "./world-config";

interface WorldHudProps {
  nearbyStation: StationConfig | null;
  mapOpen: boolean;
  onToggleMap: () => void;
  onCloseMap: () => void;
}

export function WorldHud({
  nearbyStation,
  mapOpen,
  onToggleMap,
  onCloseMap,
}: WorldHudProps) {
  return (
    <>
      <div className="world-hud" aria-label="World controls">
        <div className="world-hud-status">
          <span className="world-hud-kicker">Command Center</span>
          <span className="world-hud-help">WASD / arrows · click to move · drag to orbit · E to inspect</span>
        </div>
        <nav className="world-hud-nav" aria-label="World navigation">
          <button type="button" className="world-hud-button" onClick={onToggleMap}>
            Map
          </button>
          <Link to="/projects">Projects</Link>
          <Link to="/resume">Resume</Link>
          <Link to="/ask">Ask</Link>
          <Link to="/contact">Contact</Link>
        </nav>
      </div>

      <div className="world-nearby" aria-live="polite">
        {nearbyStation ? (
          <span>
            <kbd>E</kbd> Inspect {nearbyStation.title}
          </span>
        ) : (
          <span>Approach a glowing station to inspect it.</span>
        )}
      </div>

      {mapOpen ? (
        <section className="world-map-panel" aria-label="Portfolio world map">
          <div className="world-panel-heading">
            <div>
              <span className="world-hud-kicker">World map</span>
              <h2>Command Center online</h2>
            </div>
            <button type="button" className="world-close" onClick={onCloseMap} aria-label="Close map">
              ×
            </button>
          </div>
          <div className="world-map-grid">
            <strong>Command Center · You are here</strong>
            <span>Build Lab · locked until slice certification</span>
            <span>Automation Lab · locked until slice certification</span>
            <span>Client Street · locked until slice certification</span>
            <span>Timeline Corridor · locked until slice certification</span>
            <span>Hobby District · locked until slice certification</span>
          </div>
        </section>
      ) : null}
    </>
  );
}
