# Portfolio World Documentation Index

This directory is the canonical documentation surface for the production Portfolio World.

## Start here

For current work:

1. `../../AGENTS.md`
2. `../../CONTEXT.md`
3. `../../HANDOFF.md`
4. active workflow context under `../../workflow/active/`

## Core architecture

- `ARCHITECTURE.md` — application/world architecture and authority boundaries.
- `WORLD-SPEC.md` — zone/world behavior.
- `MOVEMENT-ARCHITECTURE.md` — movement/navigation contract.
- `RENDERING-TECHNOLOGY.md` — WebGL/WebGPU/Wasm policy.
- `ASSET-BUDGET.md` — transfer and asset ceilings.
- `CONTENT-CONTRACT.md` — factual/content authority.
- `ASK-CONTRACT.md` — grounded Ask interface and disclosure rules.
- `LOCAL-DEVELOPMENT.md` — local development/runtime checks.

## Blender visual-upgrade documents

- `BLENDER-ART-PIPELINE.md` — high-level visual upgrade sequence.
- `BLENDER-ASSET-CONTRACT.md` — hard interface between Blender assets and the runtime.
- `BLENDER-AUTHORING-GUIDE.md` — modeling/export/source-control workflow.
- `BLENDER-QA-CERTIFICATION.md` — required visual, runtime, performance and fallback gates.
- `BLENDER-STAGE-01-VALIDATION.md` — current asset-bake evidence/status.

Related decision:

- `../../decisions/2026-10-01-blender-world-art.md`

Active workflow:

- `../../workflow/active/portfolio-world-blender-art/`

## Historical certification

Files named `STAGE-*-VALIDATION.md`, `STAGE-06-BASELINE.md`, and `PROMOTION-RECORD.md` preserve evidence for the certified pre-Blender runtime.

They are historical evidence, not permission to claim the current Blender branch has passed the same gates.

## Source-of-truth rule

When documents conflict:

1. current accepted decision record;
2. current active workflow/stage contract;
3. current repository architecture/content contracts;
4. historical validation evidence.

Do not use conversation memory to override repository canon.
