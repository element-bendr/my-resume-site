import { Link } from "react-router";
import type { StationConfig } from "./world-config";
import { ZONES, ZONE_BY_ID, type ZoneId } from "./world-topology";

interface WorldHudProps {
  nearbyStation: StationConfig | null;
  currentZone: ZoneId;
  mapOpen: boolean;
  onToggleMap: () => void;
  onCloseMap: () => void;
  onFastTravel: (zone: ZoneId) => void;
}

export function WorldHud({
  nearbyStation,
  currentZone,
  mapOpen,
  onToggleMap,
  onCloseMap,
  onFastTravel,
}: WorldHudProps) {
  return (
    <>
      <div className="world-hud" aria-label="World controls">
        <div className="world-hud-status">
          <span className="world-hud-kicker">{ZONE_BY_ID[currentZone].label}</span>
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
          <span>Explore the district or open the map for fast travel.</span>
        )}
      </div>

      {mapOpen ? (
        <section className="world-map-panel" aria-label="Portfolio world map">
          <div className="world-panel-heading">
            <div>
              <span className="world-hud-kicker">World map</span>
              <h2>{ZONE_BY_ID[currentZone].label}</h2>
            </div>
            <button type="button" className="world-close" onClick={onCloseMap} aria-label="Close map">
              ×
            </button>
          </div>
          <div className="world-map-grid">
            {ZONES.map((zone) => (
              <button
                key={zone.id}
                type="button"
                className={zone.id === currentZone ? "world-map-destination is-current" : "world-map-destination"}
                onClick={() => onFastTravel(zone.id)}
              >
                <strong>{zone.label}</strong>
                <span>{zone.id === currentZone ? "You are here" : "Fast travel"}</span>
              </button>
            ))}
          </div>
        </section>
      ) : null}
    </>
  );
}
