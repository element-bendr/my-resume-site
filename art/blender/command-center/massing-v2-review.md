# Command Center Massing V2 greybox

Status: **MASSING V2 GREYBOX — REVIEW READY**. Composition acceptance is pending.

## Provenance and scope

Resumed after reconciliation `4329481` and provenance repair `5d56cdf`.
Accepted preview camera decision: `79ea3fc`. Source was reset from the failed
second pass rather than incrementally detailed. Failed source remains recoverable
from `e948434` (SHA-256 `5c6de675b176b9cc9dbb43651d35ca7f7e5a9c300943602c758eac555ad26513`).
The reset retains protected guides, coordinates, and the approved camera.

Existing MCP Blender **5.2.1 LTS** authored, validated and rendered this candidate.
No additional Blender process or installation was used. Repository production
target remains Blender 4.5 LTS; this is review evidence, not production certification.

## Composition reset

A chamfered elliptical civic island replaces the rectangular failed composition.
Four tapered underside tiers establish suspended mass. Five projecting bridges
connect to simple destination silhouette placeholders. Staggered perimeter
towers and separate terrace levels frame the central open landmark volume.
Perimeter planters, benches, trees and a spawn-position scale figure establish
foreground scale. Three neutral review materials allow shape evaluation without
production textures, emissive dressing or greebles.

The canonical perspective is `(0,-21,10)` toward `(0,0,1.6)`, FOV 52°, 1600×900,
Eevee, AgX, exposure 0. Top evidence is square 1600×1600 for the complete bridge
plan. The oblique side evidence is 1600×900 and exposes the floating underside.
The saved source restores the canonical perspective camera.

## Structural and budget validation

- Structural validation: **PASS**, zero errors.
- Export collection: **119 meshes / 29,812 triangles**.
- Review context: **31 meshes / 6,876 triangles**.
- Complete greybox: **150 meshes / 36,688 triangles**.
- Materials: **3** (`CC_SoftMetal`, `CC_Graphite`, `CC_Teal`).
- Image textures: **0**.
- Massing preferred 20k–40k and 50k soft ceiling: **PASS**.
- Production validator warns below its 35k preferred lower bound; this is expected
  for the deliberately lower-detail Massing V2 gate.
- Workflow check: **PASS**. Strict workflow status: **CURRENT**.
- Stage 02 remains blocked: `massing_v2_visual_reset_required`.

Underside, extended bridges, satellite silhouettes and the scale figure are
explicit `review_*` geometry in **PREVIEW_DO_NOT_EXPORT**. They are counted in
the complete greybox total, but are excluded from the production structural
validator. The export collection independently preserves all certified bounds,
entrance, spawn, circulation and Ask approach clearances. The floating underside
requires a later asset-contract/validator decision before production authoring;
this review does not approve exporting it.

## Comparison against finalized references

The primary reference's floating hub, radial connections, open peripheral depth
and skyline hierarchy are now represented by massing. The side view communicates
the floating island clearly; the top view proves all five bridge directions.
The core is lower than the civic towers and no longer sets the whole skyline.

Remaining visual concerns must be assessed honestly before detailing:

- The canonical perspective still gives substantial screen area to a continuous
  circular floor. The protected circulation band limits elevated scenery there.
- Tower and portal silhouettes remain regular and rectilinear; the reference has
  richer architectural variety and more integrated curved civic forms.
- The background is a simple sky fill, with no articulated sunset horizon.
- Canonical perspective crops remote bridge endpoints; the plan and side views
  demonstrate their complete relationships.
- The Ask overhead frame is recognizable as a distinct pocket but still needs
  architectural continuity after composition acceptance.
- Landscape is represented by scale masses, not final vegetation density.

These are review findings, not a visual PASS. Do not add detail until the greybox
receives explicit composition approval.

## Evidence hashes

| Artifact | SHA-256 |
| --- | --- |
| `source/command-center.blend` | `2c081a183a87e416a71954b7a6d1e2cc606daa2113605835f4e7713a7a71f76b` |
| `previews/massing-v2-runtime.png` | `a4b3e573b8ccb133ffba6ff2ae88b56874aa1e6921cb292018989755bb5444bc` |
| `previews/massing-v2-top.png` | `b0517565887920f3fec518897db15a390bd53019f7481dc54a76866bef5f0ce5` |
| `previews/massing-v2-side.png` | `e34b036dd968abc003c7e17c8c48960bd10e671fa0716d082e2712fc8033b527` |
| `massing-v2-validation.json` | `d35a4bef81bb4d29de46ea9012cb03e536039ed7db29fe8157cdd10163a8c41c` |

Structural checks ran through the existing `validate_command_center_source`
module inside the connected Blender. All three saved images were inspected.
`tools/blender/author_massing_v2.py` records the reset for reproducibility.

## Protected state and next action

Runtime files, certified movement/topology/stations/Ask/content/routes and
fallback remain unchanged. User-owned `AGENTS.md` remains untouched/uncommitted.
No production GLB export, React integration, Stage 03, push, merge or deployment.
Next action: independent Terra composition review of these three views, followed
by explicit human visual acceptance before any detailed modeling resumes.
