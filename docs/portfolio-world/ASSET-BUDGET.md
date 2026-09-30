# Asset Budget

Internal performance budgets are intentionally stricter than Cloudflare platform maximums.

| Surface | Target |
| --- | ---: |
| Critical HTML/CSS/JS shell | <= 1.5 MiB compressed |
| First visible 3D payload | <= 3 MiB compressed |
| Core first-visit transfer before optional zones | <= 5 MiB compressed |
| Individual GLB | <= 4 MiB |
| Normal texture | <= 512 KiB |
| Exceptional hero texture | <= 1 MiB |
| Individual lazy zone pack | <= 5 MiB |
| Absolute internal single-asset ceiling | 10 MiB |

Rules:
- zones load on demand;
- prefer KTX2/Basis textures and optimized GLB geometry;
- use shared materials/atlases and instancing;
- video is never critical-path media;
- target exceptions require measured evidence;
- crossing 10 MiB requires a recorded architecture exception.
