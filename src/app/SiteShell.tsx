import { useLayoutEffect, useRef } from "react";
import { NavLink, Outlet, useLocation } from "react-router";
import { identity } from "../content";
import { WorldLabelPortalContext } from "./world-label-portal";
import { primaryNavigation } from "./route-config";

export function SiteShell() {
  const portalHost = useRef<HTMLDivElement>(null);
  const location = useLocation();

  useLayoutEffect(() => {
    const host = portalHost.current;
    if (!host || !location.pathname.startsWith("/play")) {
      if (host) host.style.display = "none";
      return;
    }

    let canvas: HTMLElement | null = null;
    const align = () => {
      const nextCanvas = document.querySelector<HTMLElement>(".world-canvas");
      if (!nextCanvas) {
        host.style.display = "none";
        return;
      }
      if (canvas !== nextCanvas) {
        if (canvas) observer.unobserve(canvas);
        canvas = nextCanvas;
        observer.observe(canvas);
      }
      const bounds = canvas.getBoundingClientRect();
      Object.assign(host.style, {
        display: "block",
        left: `${bounds.left}px`,
        top: `${bounds.top}px`,
        width: `${bounds.width}px`,
        height: `${bounds.height}px`,
      });
    };

    const observer = new ResizeObserver(align);
    const mountObserver = new MutationObserver(align);
    mountObserver.observe(document.body, { childList: true, subtree: true });
    align();
    window.addEventListener("resize", align);
    window.addEventListener("scroll", align, true);
    window.visualViewport?.addEventListener("resize", align);
    window.visualViewport?.addEventListener("scroll", align);

    return () => {
      observer.disconnect();
      mountObserver.disconnect();
      window.removeEventListener("resize", align);
      window.removeEventListener("scroll", align, true);
      window.visualViewport?.removeEventListener("resize", align);
      window.visualViewport?.removeEventListener("scroll", align);
      host.style.display = "none";
    };
  }, [location.pathname]);

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

      <WorldLabelPortalContext.Provider value={portalHost}>
        <main id="main-content">
          <Outlet />
        </main>
        <div
          ref={portalHost}
          className="world-label-portal-host"
          aria-hidden="true"
          style={{
            display: "none",
            position: "fixed",
            overflow: "hidden",
            pointerEvents: "none",
            zIndex: 2,
          }}
        />
      </WorldLabelPortalContext.Provider>

      <footer className="site-footer">
        <span>{identity.name}</span>
        <span aria-hidden="true">·</span>
        <span>{identity.location}</span>
        <a href={`mailto:${identity.publicEmail}`}>{identity.publicEmail}</a>
      </footer>
    </div>
  );
}
