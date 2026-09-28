import { NavLink, Outlet } from "react-router";
import { identity } from "../content";
import { primaryNavigation } from "./route-config";

export function SiteShell() {
  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>

      <header className="site-header">
        <NavLink className="brand" to="/" aria-label="Vijay Kumaran home">
          <span className="brand-mark" aria-hidden="true">
            VK
          </span>
          <span>
            <strong>{identity.name}</strong>
            <small>{identity.consultingTitle}</small>
          </span>
        </NavLink>

        <nav aria-label="Primary">
          <ul className="nav-list">
            {primaryNavigation.map((route) => (
              <li key={route.path}>
                <NavLink
                  className={({ isActive }) =>
                    isActive ? "nav-link nav-link-active" : "nav-link"
                  }
                  to={route.path}
                >
                  {route.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main id="main-content">
        <Outlet />
      </main>

      <footer className="site-footer">
        <span>{identity.name}</span>
        <span aria-hidden="true">·</span>
        <span>{identity.location}</span>
        <a href={`mailto:${identity.publicEmail}`}>{identity.publicEmail}</a>
      </footer>
    </div>
  );
}
