# Command Center browser certification

Status: STOP — not certified.

Candidate: `3998c4c774944baec9151111cc3f628b06fde029`

Production preview: `npm run preview -- --host 127.0.0.1`

The preview health endpoint returned `{"ok":true,"service":"vijay-kumaran-portfolio-world","stage":"app-foundation"}`. The production GLB request returned HTTP 200 with 845512 bytes and SHA-256 `72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496`.

Browser evidence at 1440x1000, 1024x768, and 390x844 shows the old procedural scene, not the authored Command Center GLB. The browser recorded four CSP console errors and 254 page errors: the runtime's external Draco decoder requests are blocked by the production `connect-src 'self'` policy, and Draco WebAssembly instantiation is blocked by `script-src 'self'`. The GLB is fetched successfully but does not render.

Forced no-WebGL fallback passed its bounded check: Projects, Resume, Ask, and Contact links were present; Ask reached `/ask` with zero page errors, console errors, or failed requests.

Stop condition reached: resolving the Draco/CSP integration requires a protected runtime or asset-path change, which this evidence-only task is not authorized to make. No application, GLB, Blender, workflow, or deployment path was modified.
