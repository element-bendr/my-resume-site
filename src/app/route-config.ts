export const routeConfig = [
  { path: "/", label: "Home", nav: false },
  { path: "/play", label: "Enter World", nav: true },
  { path: "/projects", label: "Projects", nav: true },
  { path: "/resume", label: "Resume", nav: true },
  { path: "/ask", label: "Ask", nav: true },
  { path: "/contact", label: "Contact", nav: true },
] as const;

export const essentialRoutePaths = routeConfig.map((route) => route.path);
export const primaryNavigation = routeConfig.filter((route) => route.nav);
