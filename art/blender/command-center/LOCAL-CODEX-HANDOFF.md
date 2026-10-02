# Local Codex handoff — Command Center Blender authoring

## Goal

Create the first genuinely authored Blender source for Portfolio World: the Command Center.

This is local creative work. Do not substitute the Stage 01 procedural GLB for the authored source.

## Required reading order

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-blender-art/CONTEXT.md`
5. `workflow/active/portfolio-world-blender-art/02-command-center-integration-CONTEXT.md`
6. `docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`
7. `docs/portfolio-world/BLENDER-ASSET-CONTRACT.md`
8. `art/blender/command-center/README.md`

## Preconditions

- local repository checked out on `feat/blender-world-art-pipeline`;
- Blender 4.5 LTS installed locally and available as `blender`;
- Node 22.22.x / npm 11.20.x for repository validation;
- do not modify `main`.

Confirm:

```bash
blender --version
git branch --show-current
git status --short
```

## Step 1 — activate the managed stage

Stage 02 is intentionally left blocked until local execution starts.

Run:

```bash
python3 scripts/workflow_activate.py \
  --workflow portfolio-world-blender-art \
  --write
```

Then:

```bash
python3 scripts/workflow_status.py --strict
```

Expected active stage:

`02-command-center-integration`

## Step 2 — create the Blender authoring source

Run once:

```bash
npm run art:cc:bootstrap
```

This creates:

`art/blender/command-center/source/command-center.blend`

The bootstrap contains guide geometry only. Guide collections are constraints, not final art.

Open the `.blend` in Blender.

## Step 3 — author the scene

Model final Command Center scenery under:

`EXPORT_COMMAND_CENTER`

Never move protected runtime points or guide regions to make art fit.

The canonical modeling dimensions, portal clearances, material names, preview camera and quality bar live in:

`docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`

The scene must visibly exceed Stage 01 blockout quality.

## Step 4 — validate source during authoring

Run repeatedly:

```bash
npm run art:cc:validate
```

Validation rejects:

- missing required architectural objects;
- illegal collection structure;
- excessive triangles/materials;
- out-of-bounds geometry;
- player-height geometry in protected bridge/spawn/Ask areas;
- player-height geometry in the main circulation annulus;
- cameras/lights in the export collection.

Do not weaken validation to make a model pass. Fix the model.

## Step 5 — render canonical preview

Run:

```bash
npm run art:cc:preview
```

Review:

`art/blender/command-center/previews/runtime.png`

This render uses the runtime-matched camera.

Do not export to runtime merely because structural validation passes. The render must also pass the visual criteria in the spec.

## Step 6 — visual refinement loop

Compare the render against the frozen authoring specification and, when available, the approved reference image.

Reject and refine when the room still reads as:

- primitive blocks;
- one cylinder plus torus hologram;
- featureless box walls;
- flat perimeter slabs;
- emissive strips hiding weak architecture.

Stop after two materially similar failed approaches and revise the design/source rule rather than endlessly adding detail.

## Step 7 — export only after visual PASS

Run:

```bash
npm run art:cc:validate
npm run art:cc:preview
npm run art:cc:export
npm run art:verify
```

The production asset is:

`public/world/art/command-center.glb`

The `.blend` remains the authoritative art source.

## Step 8 — evidence before React integration

Record:

- Blender version;
- `.blend` SHA-256;
- GLB SHA-256;
- validation report;
- triangle/material counts;
- `runtime.png`;
- visual verdict;
- exact Git candidate.

Only after the visual verdict is PASS may Stage 02 modify `src/world/CommandCenter.tsx` to consume the GLB.

## Protected state

Do not change:

- world bounds;
- bridge bounds;
- player spawn;
- Ask station position or interaction point;
- movement/controller rules;
- camera contract;
- content/Ask facts;
- production deployment;
- `main`.

## Stop condition

If the authored scene cannot satisfy the guide clearances and the intended visual language simultaneously, stop and update the Stage 02 design contract. Do not silently change runtime behavior.