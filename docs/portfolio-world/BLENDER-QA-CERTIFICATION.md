# Blender Visual and Runtime Certification

## Purpose

Define the evidence required before Blender-authored scenery can replace the certified primitive visuals.

A screenshot that “looks nicer” is not certification. Apparently we need to write that down.

## Gate A — source and asset integrity

Required:

- Blender version pinned;
- asset has reproducible source;
- expected file name/path;
- GLB parses successfully;
- asset budget passes;
- no camera/light export unless explicitly approved;
- no secret/private content embedded in extras, node names or textures.

## Gate B — visual fidelity

Inspect the actual production camera at:

- 1440px desktop;
- 1024px;
- 768px;
- 390px mobile;
- 360px mobile.

Check:

- silhouette resembles approved art direction;
- no obvious primitive/blocky placeholder remains in the replaced zone;
- no clipping/z-fighting;
- emissive surfaces are legible but not blown out;
- station labels remain readable;
- avatar/player remains visually separable from the environment;
- scene still communicates the zone's resume function.

## Gate C — interaction regression

For every replaced district:

- keyboard movement works;
- click/tap-to-move works;
- movement remains inside certified walkable bounds;
- fast travel arrives in the expected zone;
- station proximity still activates the same interaction;
- no decorative mesh steals pointer events;
- opening/closing interaction UI does not corrupt movement;
- route exits remain clean.

## Gate D — performance

Measure from a production build, not Blender.

Required evidence:

- initial `/play` transfer;
- GLB transfer size;
- GLB decode/load duration where measurable;
- total JS budget remains within existing limit;
- no long frame hitch that materially harms movement;
- desktop target: stable 60 FPS on representative hardware where practical;
- mobile target: usable 45–60 FPS with quality reduction available;
- no unbounded GPU-memory growth when travelling between zones.

Quality may be reduced before changing interaction behavior.

## Gate E — accessibility and fallback

Required:

- conventional Resume/Projects/Ask/Contact routes unchanged;
- keyboard/focus behavior unchanged;
- reduced-motion behavior unchanged;
- coarse-pointer/touch targets unchanged;
- forced no-WebGL fallback still reaches essential routes;
- GLB failure does not create a blank application.

## Gate F — console/network

Required:

- zero application page errors;
- zero unexpected failed requests;
- no repeated 404 loop for an asset;
- no raw stack/error overlay shown to normal visitors;
- expected cacheable static asset behavior.

## Gate G — promotion

A district visual may replace its primitive fallback only when Gates A–F pass for the exact candidate.

Repository-wide merge requires:

```bash
python3 scripts/bootstrap_check.py
python3 scripts/workflow_check.py
python3 scripts/workflow_status.py --strict
npm run verify:offline
npm run typecheck
npm test
npm run build
npm run verify:assets
npm run verify:world-assets
npm run art:verify
npm run verify:ask-disclosure
npm run verify:world-ask
```

Browser evidence then covers the existing route matrix plus the Blender-specific checks above.

Production deployment remains a separate explicit promotion step.
