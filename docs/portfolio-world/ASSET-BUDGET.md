# Asset Budget

Internal performance budgets are intentionally stricter than Cloudflare platform maximums.

| Surface | Target |
| --- | ---: |
| Critical HTML/CSS/JS shell | <= 1.5 MiB compressed |
| First visible 3D payload | <= 3 MiB compressed |
| Core first-visit transfer before optional zones | <= 5 MiB compressed |
| Individual production GLB hard target | <= 4 MiB |
| Blender Stage 01 untextured GLB | <= 900 KiB each |
| Blender Stage 01 six-GLB total | <= 4 MiB |
| Normal texture | <= 512 KiB |
| Exceptional hero texture | <= 1 MiB |
| Individual lazy zone pack | <= 5 MiB |
| Absolute internal single-asset ceiling | 10 MiB |

## Rules

- zones load on demand;
- initial Command Center must not force-download all district GLBs;
- prefer KTX2/Basis textures and optimized GLB geometry;
- use shared materials/atlases and instancing;
- video is never critical-path media;
- decoder/transcoder/Wasm payloads count toward transfer budgets;
- target exceptions require measured evidence;
- crossing the 4 MiB normal GLB target requires explicit performance evidence;
- crossing 10 MiB requires a recorded architecture exception.

## Blender staged budgets

Stage 01 deliberately uses a tighter `900 KiB` per-file ceiling because the generated baseline has no image textures. It is a geometry/material sanity gate, not the permanent textured-zone allowance.

When textures/LODs are introduced later, total lazy zone cost is measured as the complete required pack:

```text
GLB
+ textures
+ decoder/transcoder cost attributable to the route
+ zone-specific JS
```

A visually impressive district that quietly turns a portfolio visit into a game download has failed the brief.
