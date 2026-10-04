# Command Center Detail Review

## Reference comparison

The detailed candidate preserves the accepted Massing V2 composition and preview camera while adding the authored cues requested for the civic hub: layered facade bays and ledges on the background civic hall, curved lateral canopies, a layered cyan structural crown around the hero core, foreground lamps/seating, perimeter planting, and a compressed suspended-edge treatment. The runtime view retains foreground, midground, and background separation, the five lateral/diagonal destination directions, the central civic plaza, and visible sky around the floating platform.

Canonical evidence:

- `previews/detail-runtime.png` — approved runtime camera composition.
- `previews/detail-top.png` — plan/terrace and destination layout.
- `previews/detail-side.png` — elevation, vertical hierarchy, and floating edge.

## Source validation

- Blender: 5.2.1 LTS (local authoring executable).
- Source: `source/command-center.blend`.
- Result: `PASS`.
- Export collection: 209 mesh objects, 48,236 triangles, 5 approved materials.
- Preview-only bridge, destination, scale, and lighting objects remain outside `EXPORT_COMMAND_CENTER`.
- Production export was intentionally not run.

## Protected state

- Massing V2 spatial foundation, spawn, Ask clearances, bridge entrances, topology, and runtime camera behavior were not changed.
- Runtime camera remains `(0, -21, 10)` aimed at `(0, 0, 1.6)` with 52° FOV.
- No React files, production GLB, protected references, workflow state, or `AGENTS.md` were changed.

## Known limitations

- Materials remain intentionally restrained and texture-free; this is a detailed authored review candidate, not production export polish.
- The underside treatment is a bounded visual edge/brace treatment rather than a full structural simulation.
- Terra independent visual review is still required before any later export task.
