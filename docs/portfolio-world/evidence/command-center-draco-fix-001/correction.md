# Command Center Draco correction

Status: bounded runtime correction candidate.

- Base/runtime candidate SHA: `3998c4c774944baec9151111cc3f628b06fde029`.
- Failed browser-certification evidence remains at candidate `bee352c0c2cf81f7564fb6b61864dc693cdb6720`, recorded in `command-center-browser-cert-001/runtime-certification.md` and `browser-evidence.json`.
- Production asset remains `public/world/art/command-center.glb`, 845512 bytes, SHA-256 `72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496`.
- Decoder provenance: `three@0.186.0`; source `node_modules/three/examples/jsm/libs/draco/gltf/draco_decoder.js`; destination `public/draco/draco_decoder.js`.
- Runtime boundary: `CommandCenterArt.tsx` owns a dedicated JavaScript `DRACOLoader` at `/draco/`, disables Drei's default Draco loader, and injects the dedicated loader through `useGLTF`'s extension hook. The loader uses the installed `three-stdlib` export required by Drei's GLTF loader type contract.
- CSP, Blender source, topology, movement, spawn, bridge, camera, Ask, stations, content, HUD, and production GLB are unchanged.

Validation before commit: focused runtime test 6/6; `command-center-draco-local` PASS; `blender-assets` PASS; `npm run verify` PASS (13 files, 74 tests, build, asset budgets); `icm-stage` PASS. The local Draco guard was executed from the repository's existing validator commit because that validator script is outside this task's authorized write paths.
