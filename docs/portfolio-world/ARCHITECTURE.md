# Portfolio World Architecture

## Experience model
Two first-class modes:
1. **World mode** — stylized 3D walkthrough.
2. **Portfolio mode** — conventional HTML for recruiters, SEO, accessibility, weak devices, and direct navigation.

World zones:
- Command Center — identity and primary navigation
- Build Lab — production systems/projects
- Automation Lab — AI agents/workflows/infrastructure
- Client Street — shipped client work
- Timeline Corridor — experience/milestones
- Hobby District — gaming, anime, kettlebells, philosophy, tinkering
- Ask Terminal — grounded questions about project evidence

## Runtime
```text
Browser
  ├─ React / TypeScript / Vite
  ├─ React Three Fiber / Three.js / Drei
  ├─ HTML HUD + accessible fallback routes
  └─ lazy-loaded zone assets
          │
          ▼
Cloudflare Worker
  ├─ Static Assets
  └─ dynamic API routes only
```

## Content rule
Resume and project facts live in structured content, not scene components. The 3D world renders verified content; it does not become a second factual source.

## Rendering rules
- low-poly/stylized over photorealistic;
- baked lighting before runtime lighting;
- instancing/shared materials for repeated props;
- lazy zone loading;
- adaptive/on-demand rendering;
- no heavyweight physics without a concrete interaction need;
- no interaction may obstruct direct resume/project access.

## Promotion
`main` remains protected. Preview and certification occur from the feature branch. Production promotion is explicit and evidence-backed.
