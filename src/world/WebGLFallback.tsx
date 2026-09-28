import { Link } from "react-router";

export function WebGLFallback() {
  return (
    <div className="world-webgl-fallback" role="status">
      <div>
        <span className="world-hud-kicker">3D unavailable</span>
        <h2>Use the conventional portfolio.</h2>
        <p>
          This browser could not create a stable WebGL context. The professional content remains
          fully available without the 3D layer.
        </p>
        <div className="action-row">
          <Link className="button button-primary" to="/projects">
            Projects
          </Link>
          <Link className="button button-secondary" to="/resume">
            Resume
          </Link>
          <Link className="button button-secondary" to="/ask">
            Ask
          </Link>
          <Link className="button button-secondary" to="/contact">
            Contact
          </Link>
        </div>
      </div>
    </div>
  );
}
