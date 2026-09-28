# Portfolio World Architecture

## Experience model

Two first-class modes:
1. **World mode** — stylized 3D walkthrough.
2. **Portfolio mode** — conventional HTML for recruiters, SEO, accessibility, weak devices, and direct navigation.

The world and movement contracts are defined in:
- `docs/portfolio-world/WORLD-SPEC.md`
- `docs/portfolio-world/MOVEMENT-ARCHITECTURE.md`
- `docs/portfolio-world/ASSET-BUDGET.md`

## World zones

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
  ├─ HTML portfolio/resume routes
  ├─ React Three Fiber / Three.js / Drei
  │    ├─ PlayerController
  │    ├─ NavigationController
  │    ├─ Character
  │    ├─ FollowCamera
  │    ├─ InteractionController
  │    └─ lazy-loaded world zones
  │
  ▼
Cloudflare Worker
  ├─ Static Assets
  └─ dynamic API routes only
```

## Movement contract

World movement is guided third-person exploration:
- keyboard + click-to-move on desktop;
- tap-to-move on mobile;
- legal movement constrained by navmesh/navigation graph;
- map fast travel;
- context interaction points;
- no jumping, combat, falling, or mandatory physics.

The command-center vertical slice must prove this controller before additional zones are built.

## Content rule

Resume and project facts live in structured content, not scene components. The 3D world renders verified content; it does not become a second factual source.

Substantive text and forms render as HTML overlays or normal routes, not texture-bound 3D paragraphs.

## Rendering rules

- low-poly/stylized over photorealistic;
- baked lighting before runtime lighting;
- instancing/shared materials for repeated props;
- lazy zone loading;
- adaptive/on-demand rendering;
- no heavyweight physics without a concrete interaction need;
- no interaction may obstruct direct resume/project access.

## Failure and fallback

The 3D experience is enhancement, not authority.

If WebGL, navigation, an asset, or the world controller fails:
- essential Resume, Projects, Ask, and Contact surfaces remain directly accessible;
- a failed path query never moves the avatar through geometry;
- low-power/reduced-motion behavior preserves content reachability.

## Promotion

`main` remains protected. Preview and certification occur from the feature branch. Production promotion is explicit and evidence-backed.
