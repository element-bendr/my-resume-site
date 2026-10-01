# Portfolio World Architecture

## Experience model

Two first-class modes:

1. **World mode** — stylized interactive 3D walkthrough.
2. **Portfolio mode** — conventional HTML for recruiters, SEO, accessibility, weak devices and direct navigation.

The world and movement contracts are defined in:

- `docs/portfolio-world/WORLD-SPEC.md`
- `docs/portfolio-world/MOVEMENT-ARCHITECTURE.md`
- `docs/portfolio-world/ASSET-BUDGET.md`
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`

The authored visual layer is additionally defined in:

- `decisions/2026-10-01-blender-world-art.md`
- `docs/portfolio-world/BLENDER-ART-PIPELINE.md`
- `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
- `docs/portfolio-world/BLENDER-AUTHORING-GUIDE.md`
- `docs/portfolio-world/BLENDER-QA-CERTIFICATION.md`

## World zones

- Command Center — identity and primary navigation
- Build Lab — production systems/projects
- Automation Lab — AI agents/workflows/infrastructure
- Client Street — shipped client work
- Timeline Corridor — experience/milestones
- Hobby District — gaming, anime, kettlebells, philosophy, tinkering
- Ask Terminal — grounded questions about project evidence

## Runtime and art-authoring split

```text
Concept / art direction
        │
        ▼
Blender 4.5 LTS
        │
        ├─ authored geometry
        ├─ PBR material intent
        ├─ UV / bake source
        └─ LOD source
        │
        ▼
GLB / glTF 2.0 per district
        │
        ▼
Browser
  ├─ React / TypeScript / Vite
  ├─ HTML portfolio/resume routes
  ├─ React Three Fiber / Three.js / Drei
  │    ├─ WebGL 2 production renderer
  │    ├─ Blender scenery loader
  │    ├─ PlayerController
  │    ├─ certified topology / movement
  │    ├─ interaction stations
  │    ├─ follow camera
  │    └─ lazy-loaded world zones
  │
  ▼
Cloudflare Worker
  ├─ Static Assets
  └─ dynamic API routes only
```

Blender does not own navigation, collision, interaction coordinates or factual portfolio content.

## Movement contract

World movement is guided third-person exploration:

- keyboard + click-to-move on desktop;
- tap-to-move on mobile;
- legal movement constrained by the certified application topology;
- map fast travel;
- context interaction points;
- no jumping, combat, falling or mandatory physics.

Authored scenery must fit this contract. The runtime contract is not stretched merely because a model is inconveniently large.

## Content rule

Resume and project facts live in structured content, not scene components or Blender text. The 3D world renders verified content; it does not become a second factual source.

Substantive text and forms render as HTML overlays or normal routes, not texture-bound 3D paragraphs.

## Rendering technology

- WebGL 2 is the production renderer;
- WebGPU remains architecture-ready and optional;
- WebAssembly may be used selectively for mature codecs/helpers with measured benefit;
- movement, navigation, content, interaction and UI remain renderer-independent;
- conventional HTML remains the final fallback tier.

See `docs/portfolio-world/RENDERING-TECHNOLOGY.md`.

## Rendering rules

- authored stylization over photorealism-for-its-own-sake;
- bevels/curves/material response instead of exposed primitive blocks for hero scenery;
- baked detail before runtime geometry where appropriate;
- instancing/shared materials for repeated props;
- lazy zone loading;
- adaptive/on-demand rendering;
- bounded post-processing;
- no heavyweight physics without a concrete interaction need;
- no interaction may obstruct direct resume/project access.

## Failure and fallback

The 3D experience is enhancement, not authority.

If WebGL, navigation, a GLB, texture or world controller fails:

- essential Resume, Projects, Ask and Contact surfaces remain directly accessible;
- a failed path query never moves the avatar through geometry;
- an unproven Blender asset does not replace its certified fallback;
- low-power/reduced-motion behavior preserves content reachability.

## Promotion

`main` remains protected. Art, runtime integration and certification occur on isolated branches. Merge and production deployment are separate evidence-backed authority transfers.
