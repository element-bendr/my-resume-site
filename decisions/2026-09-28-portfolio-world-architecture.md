# Decision: Build the resume as an optional 3D portfolio world on Cloudflare Workers

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context
The existing repository must remain intact on `main` while the new interactive version is developed. The desired experience is a stylized 3D walkthrough presenting resume content, production projects, client work, hobbies, and the Ask-about-the-work concept without forcing recruiters to navigate a game to reach the resume.

Cloudflare's 25 MiB Workers Static Assets limit is per individual static asset, not a 25 MiB total-account limit.

## Decision
1. Build on `feat/portfolio-world-icm-rebuild`; do not modify `main` before certification.
2. Use React + TypeScript + Vite with React Three Fiber/Drei.
3. Keep conventional portfolio, projects, resume, Ask, and contact routes directly accessible.
4. Use Workers Static Assets; Worker code handles only dynamic API paths.
5. Do not add D1, KV, Durable Objects, R2, or a second Cloudflare account without measured need.
6. Lazy-load zones and use stylized optimized assets.
7. Internal budgets: shell <=1.5 MiB compressed; first visible 3D <=3 MiB; core first visit <=5 MiB; GLB target <=4 MiB; normal texture <=512 KiB; hero texture <=1 MiB; lazy zone <=5 MiB; no asset >10 MiB without a recorded exception.
8. Prefer Meshopt/Draco where useful, KTX2/Basis textures, instancing, baked lighting, and adaptive/on-demand rendering.
9. Provide mobile, low-power, reduced-motion, and non-WebGL paths.
10. Promote only after tests, build, budget checks, accessibility, visual inspection, and Cloudflare preview certification.

## Consequences
- The portfolio can be memorable without making 3D mandatory.
- Asset size becomes a measurable engineering constraint.
- Existing Cloudflare account remains viable unless future evidence shows otherwise.

## Validation / evidence
- baseline commit: 63d25e7dbc3169cb41aaa181a513ca7af5860ba4
- ICM template source: 90322a2441539f24eafdbd2c8a36bc6392192af4
- Cloudflare limits must be rechecked again at production certification.

## Revisit when
- a required asset cannot meet the internal ceiling after reasonable optimization;
- measured first-load performance requires a different delivery architecture;
- Ask integration requires a capability outside the chosen Worker design.
