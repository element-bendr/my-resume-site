# Command Center Massing V2 Plan

status: REQUIRED_AFTER_TWO_ATTEMPT_VISUAL_FAIL
stage: 02-command-center-integration
scope: composition reset only

## Why this exists

The first two authored Command Center attempts passed structural validation but failed visual review.

Recorded local evidence supplied by the authoring session:

- camera decision: `79ea3fc`
- second-pass checkpoint: `e948434`
- structural validation: PASS
- scene size: 296 meshes
- triangle count: 105,600
- materials: 6
- Terra visual review: FAIL
- local evidence file: `/mnt/shared/projects/mixed/Resume-gamified/.worktrees/blender-world-art/art/blender/command-center/visual-pass-02.md`
- mandatory two-attempt stop rule: triggered

No GLB export, React integration, push, merge, deployment, or `main` change occurred from the failed local passes.

The failure is compositional, not structural:

> The scene remains a flat diorama rather than the referenced floating civic hub.

A third incremental detail pass is prohibited.

## Objective

Reset the Command Center around a new massing/composition plan that proves the floating civic-hub spatial hierarchy in cheap greybox form before detailed modeling resumes.

The next milestone is:

`COMMAND CENTER MASSING V2 — COMPOSITION REVIEW READY`

It is not:

- production GLB export;
- runtime integration;
- materials polish;
- Stage 03 district rollout.

## Core design correction

Treat the Command Center as a small floating civic district, not as a room or single platform.

The new composition must establish:

1. visible vertical hierarchy;
2. multiple elevation levels;
3. foreground / midground / background depth;
4. visible sky/horizon and floating-world void;
5. five readable outward destination directions;
6. architectural framing around the central hero core;
7. human-scale environmental cues;
8. a player-scale civic plaza rather than a flat diorama.

## Required massing layers

### Foreground

From the canonical runtime camera, show at least three of:

- player;
- railing;
- planter/vegetation mass;
- bench or lamp;
- plaza edge;
- stair/ramp edge.

The foreground must establish scale immediately.

### Midground

Must contain:

- central command dais;
- hero holographic/system core;
- multi-level plaza terraces;
- at least one finished bridge mouth;
- primary structural ribs/portal frames.

The hero core may not dominate the entire vertical frame.

### Background

Must contain:

- elevated/taller civic architecture;
- at least three destination silhouettes or portal directions;
- visible sky/horizon;
- gaps revealing depth around or beneath floating platforms.

The frame must not terminate in a continuous flat wall.

## Elevation strategy

At least three meaningful architectural levels must be visible from `PREVIEW_RUNTIME`.

Suggested runtime elevation bands:

- lower/service edge: `Y -0.6 .. 0.0`
- primary plaza: `Y 0.0 .. 0.35`
- raised civic terraces: `Y 0.6 .. 1.4`
- tower/portal/rib structures: `Y 2.4 .. 5.2`

These bands are composition guidance only. Protected movement surfaces remain runtime-owned and must not be changed.

## Floating-world requirement

The next greybox must visibly demonstrate that the hub is floating.

Required visual cues:

- deliberate island/platform edge;
- underside massing;
- at least one visible gap/void around platform geometry;
- at least one bridge projecting toward another destination;
- horizon or atmospheric background;
- no full-frame floor slab.

## Portal strategy

Five exits remain protected by the existing topology.

Each exit must receive a distinct massing cue:

- Client Street: warm/commercial frame;
- Hobby District: playful/garden-studio frame;
- Timeline: archive/monumental frame;
- Build Lab: technical/industrial frame;
- Automation Lab: operations/system frame.

At greybox stage, distinction should come from silhouette, height, massing and framing, not detailed materials.

## Central hero hierarchy

The hero core should be the focal landmark, but not the room.

Target visual hierarchy:

1. civic architecture / skyline;
2. central plaza composition;
3. system core;
4. portals / bridges;
5. human-scale props.

If the eye reads “hologram on a platform” first and “floating civic hub” second, the massing has failed.

## Greybox triangle discipline

Do not spend another 100k triangles before composition approval.

Target for Massing V2 greybox:

- preferred: `20,000 .. 40,000` triangles
- soft ceiling: `50,000` triangles
- materials: 1–3 simple review materials
- no production textures required
- no detailed greebles
- no small props beyond scale cues

The point is to make failure cheap.

## Required Massing V2 outputs

Before detailed authoring resumes, produce all of:

1. `massing-v2-top.png`
   - top/plan view
   - protected entrances visible
   - circulation/clearance relationship understandable

2. `massing-v2-runtime.png`
   - canonical runtime camera
   - principal composition review

3. `massing-v2-side.png`
   - side/elevation silhouette
   - shows vertical layering and floating underside

4. validation report
   - protected clearances
   - triangle count
   - material count

5. short written comparison against the finalized references

Suggested local paths:

```text
art/blender/command-center/previews/massing-v2-top.png
art/blender/command-center/previews/massing-v2-runtime.png
art/blender/command-center/previews/massing-v2-side.png
art/blender/command-center/massing-v2-review.md
```

## Massing V2 acceptance gate

PASS only if the greybox already demonstrates:

- floating civic-hub composition;
- visible sky/horizon;
- clear foreground/midground/background separation;
- at least three visible outward destination directions from runtime view;
- multi-level plaza;
- meaningful vertical skyline;
- at least one convincing bridge/bridge mouth;
- central hero core proportionate to the architecture;
- visible human-scale cues;
- protected movement/Ask/entrance clearances intact;
- no large empty floor area dominating the frame.

If these are not visible in greybox form, do not add detail.

## Mandatory stop rule

The two previous authored approaches already consumed the allowed incremental attempts.

Therefore the next work must be materially different in massing/composition.

Forbidden next actions:

- third incremental polish pass on the failed scene;
- adding more greebles to the same silhouette;
- adding bloom/fog to conceal flat composition;
- exporting the failed source to production;
- integrating the failed GLB into React;
- proceeding to Stage 03.

If Massing V2 greybox fails composition review, stop again and revise the spatial concept before detailed authoring.

## Protected state

Do not change:

- `src/world/world-topology.ts` semantics;
- five bridge bounds;
- player spawn;
- Ask station or interaction point;
- movement/controller semantics;
- camera runtime contract unless separately approved;
- portfolio/Ask content;
- fallback behavior;
- production;
- `main`;
- user-owned `AGENTS.md`.

## Resume condition

Detailed Blender authoring may resume only after:

`MASSING V2 GREYBOX — VISUAL PASS`

That pass must precede production materials, final geometry, GLB export, or runtime integration.