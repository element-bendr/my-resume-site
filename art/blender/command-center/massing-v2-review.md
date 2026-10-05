# Revised civic-hub massing greybox

Status: **HUMAN COMPOSITION PASS** at `dbc8d7c18fdf7b6d6761e79dbcff329f33ccda5f`.
Recorded in PR #21 comment [5956821330](https://github.com/element-bendr/my-resume-site/pull/21#issuecomment-5956821330). Stage 02 is ACTIVE for detailed Command Center authoring, not complete/certified. Production GLB export, React integration, Stage 03, merge and deployment remain blocked by later gates.

## Authority and provenance

This revision follows human rejection of the first Massing V2 composition.
Rejected source and evidence remain preserved in commit `5f6fa43`.
Remote recovery guidance was reconciled at `e3b6979113face7b9773c6a5d39003fb99512a39`.
Camera decision `79ea3fc` and camera-spec blob
`ad805aef758ace9f2fee9dca4e7dd69f28313cfb` are unchanged.
The single existing MCP-connected Blender 5.2.1 LTS application authored/rendered
this candidate. Repository production target remains Blender 4.5 LTS.

## Composition reset

The broad elliptical disc is replaced by a compact octagonal civic plaza, five
narrower threshold causeways and visible gaps between separate perimeter terraces.
Suspended service blocks and split front keels are visible from the canonical
runtime perspective. Three substantial, unequal-height/width civic buildings form
a rear skyline behind the unchanged hero core. A western civic gallery, upper
house and deep canopy frame Client Street as an occupied architectural threshold.
Raised foreground landscape terraces and benches flank protected spawn. Retaining
blocks, access stairs and stepped underside bodies distinguish lower service,
primary plaza, raised terrace and civic-building levels.

Hero core/dais dimensions are unchanged. Five bridge directions remain visible in
plan. Destination context uses broad paired wings/gates rather than lone pylons;
it is review scenery, not Stage 03 district art. No greeble or production texture
pass was performed.

## Validation and budget

- Export collection: **98 meshes / 24,228 triangles**.
- Review context: **51 meshes / 10,120 triangles**.
- Complete greybox: **149 meshes / 34,348 triangles**.
- Materials: **3** (`CC_SoftMetal`, `CC_Graphite`, `CC_Teal`).
- Production/image textures: **0**; render-result buffers are not textures.
- Structural validation: **PASS**, zero errors.
- Complete-greybox 20k–40k preferred and 50k ceiling: **PASS**.
- Workflow strict status: **CURRENT**; Stage 02 active for detailed authoring after human composition PASS.

The production-validator warning below 35k export triangles is expected for this
cheap composition gate. No clearance/budget was relaxed. Guides are unchanged.
Raised geometry preserves circulation, five entrances, spawn and Ask approach.
Suspended service masses, extended bridges, destination silhouettes and scale
figure are `review_*` geometry in `PREVIEW_DO_NOT_EXPORT`; they require a later
asset-contract decision before production authoring/export. Their triangles are
included in the complete count.

## Evidence and candid limits

All three images were rendered and inspected:

- Runtime: canonical `(0,-21,10)` toward `(0,0,1.6)`, FOV 52°, 1600×900,
  Eevee, AgX, exposure 0.
- Top: orthographic complete bridge plan, 1600×1600.
- Side: oblique floating/terrace view, 1600×900.

Saved source restores the canonical camera. This is review evidence, not human
visual acceptance. The plaza still occupies meaningful screen area; the foreground
Timeline portal partly overlaps the scale figure; lateral destination ends are
cropped in the runtime view. Access stairs read more clearly in oblique evidence.
Human review accepted the skyline, thresholds, terraces and floating gaps.
The listed non-blocking limits carry into detailed authoring; the approved camera
and player spawn must remain unchanged.

## Artifact SHA-256

| Artifact | SHA-256 |
| --- | --- |
| `source/command-center.blend` | `e6a035dc9a10a3a46c7001dec50f5dbb2820845131db74d85a166cd75cb4e6e4` |
| `previews/massing-v2-runtime.png` | `a820cb7d44334cb4c3e04c5f6e7658f7af166ce48d84832a2d59d7af3527b4e1` |
| `previews/massing-v2-top.png` | `3946105fe3cd119685d958a0f19f636414eb301b3304f347ea890c472f25863f` |
| `previews/massing-v2-side.png` | `61c938e7e6bd30e9ba7bee1ea7392c8aa6ccc868ac0e388391c5ef359fa0ba57` |
| `massing-v2-validation.json` | `cfd5a6d30afa48455af393229f33ded44eb213f50f0ee02d2d68532fbc9ed397` |

Reproduction: execute `tools/blender/author_civic_hub_revision.py` in connected
Blender. Validation uses existing `validate_command_center_source.validate`.

## Protected state and next action

Runtime camera/movement/topology/stations, Ask, content, routing and fallback
remain unchanged. User-owned `AGENTS.md` is untouched and unstaged.
No GLB export, React integration, Stage 03, merge or deployment occurred.
Next: detailed authoring on the approved composition, source/clearance validation,
runtime/top/side visual evidence and independent detailed visual review. Human
composition acceptance does not establish production-source/export readiness.
