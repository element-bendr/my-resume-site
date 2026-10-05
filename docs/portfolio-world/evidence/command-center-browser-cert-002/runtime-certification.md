# Command Center browser certification

Status: PASS — certified.

## Candidate and preserved history

- Exact candidate: `b5e27e729e6481bc98875177057fc0a193aef7ce`.
- Historical failed browser candidate preserved and referenced: `bee352c0c2cf81f7564fb6b61864dc693cdb6720`.
- No application, decoder, GLB, CSP, Blender, or deployment path changed.
- `public/_headers` unchanged.

## Protected runtime inputs

- `public/world/art/command-center.glb`: 845512 bytes, SHA-256 `72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496`.
- `public/draco/draco_decoder.js`: 512465 bytes, SHA-256 `8625489da79a805f4f2a7d511c3e52d8b4085608a9d2a4d5f4f9de5db0aea04f`.
- Runtime requests the decoder from same-origin `/draco/draco_decoder.js` with JavaScript decoding; no Google/gstatic decoder request and no WebAssembly/CSP decoder failure observed.

## Pre-certification validation

- `command-center-draco-local`: PASS — exact GLB/decoder hashes and same-origin JavaScript Draco wiring.
- `blender-assets`: PASS — `npm run art:verify`.
- `runtime-integration`: PASS — `npm run verify`; 13 test files, 74 tests, build, asset budget, and world budget passed.
- `icm-stage`: PASS — `python3 scripts/workflow_status.py --strict`.
- ICM graph validation: PASS — `python3 scripts/icm.py --json validate`.

## Browser evidence

Production preview: `npm run preview -- --host 127.0.0.1`.

Health returned HTTP 200 with `ok: true`. Chromium `153.0.8010.12` at 1440x1000, 1024x768, and 390x844 fetched the certified GLB and local decoder successfully. The authored floating civic hub rendered at all three sizes; the old procedural/fallback presentation was not dominant. Map/HUD controls, Ask Terminal, movement target feedback, and destination readability remained usable. Mobile had no horizontal overflow.

- `desktop-1440.png`
- `desktop-1024.png`
- `mobile-390.png`
- `fallback.png`
- `browser-evidence.json`

Ask Terminal reached `/ask`; a SPA exit from `/play` to `/projects` completed with zero page errors, console errors, failed requests, or HTTP failures. Forced non-WebGL fallback exposed Projects, Resume, Ask, and Contact; Ask reached `/ask` with zero errors.

Detailed machine-readable results are in `browser-evidence.json`.
