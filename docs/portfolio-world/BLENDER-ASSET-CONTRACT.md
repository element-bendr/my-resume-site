# Blender Asset Contract

## Purpose

This is the hard interface between Blender-authored scenery and the certified Portfolio World runtime.

If an asset violates this contract, the runtime must not be changed merely to accommodate the asset. Fix the asset or record an explicit architecture decision.

## Asset ownership

One production GLB per world zone:

| Zone | File | Runtime anchor |
| --- | --- | --- |
| Command Center | `command-center.glb` | `[0, 0, 0]` |
| Build Lab | `build-lab.glb` | `[-9, 0, -16]` |
| Automation Lab | `automation-lab.glb` | `[9, 0, -16]` |
| Client Street | `client-street.glb` | `[-17, 0, 0]` |
| Timeline Corridor | `timeline.glb` | `[0, 0, 17]` |
| Hobby District | `hobby-district.glb` | `[17, 0, 0]` |

The anchor is a visual placement. It does not replace the topology in `src/world/world-topology.ts`.

## Coordinate convention

Portfolio runtime coordinates are:

- X: world left/right;
- Y: world up;
- Z: world depth.

Blender authoring is Z-up. The generator treats authored location tuples as `(world X, world Z, world Y)` and converts them to Blender coordinates before export. The GLTF exporter then produces the runtime Y-up result.

Do not compensate for axis conversion by changing movement/topology coordinates.

## Origin and transform rules

- Every zone exports around a scene-local origin.
- Runtime placement happens through the zone anchor.
- Apply object scale before export.
- Avoid negative scale.
- Avoid parent transforms whose only purpose is to repair an incorrect origin.
- Do not export cameras or lights.
- Do not export collision/nav meshes as runtime authority.
- Decorative meshes must not intercept application pointer interactions unless explicitly intended.

## Naming

Use lowercase semantic names in Blender source and deterministic generator names where practical.

Preferred examples:

```text
platform
rear_wall
archive_bay
archive_screen
agent_pod
runtime_panel
shop_shell
timeline_pillar
hobby_stage
```

Names should describe function or visual role, not temporary modeling history such as `Cube.017`.

## Materials

Production materials should remain compatible with glTF PBR:

- base color;
- metallic;
- roughness;
- normal;
- ambient occlusion where useful;
- emissive where useful.

Avoid Blender-only shader graphs that cannot be represented or baked into the production asset.

First-pass generated assets intentionally use material values without image textures. Later textured assets must follow the texture compression rules below.

## Texture contract

When image textures are introduced:

- KTX2/Basis is the production target where browser support/tooling permits;
- 2K is an exception, not a default;
- repeated props should share atlases/materials;
- normal maps require visible benefit;
- alpha textures require a concrete visual need;
- decorative detail that can be baked should not become runtime geometry by habit.

Target budgets remain governed by `docs/portfolio-world/ASSET-BUDGET.md`.

## Geometry contract

- bevel visible hard-surface edges rather than relying on razor-sharp cubes;
- use smooth shading where it improves curved forms;
- remove unseen/internal geometry when material;
- repeated visual props should be instanced or duplicated economically;
- high-frequency detail belongs in textures/normal maps before excessive geometry;
- hero objects may receive more geometry only when visible from the production camera.

## Export contract

Canonical output format: binary glTF 2.0 (`.glb`).

Required exporter intent:

```text
format: GLB
selection: authored zone only
apply transforms: yes
materials: export
Y-up conversion: yes
cameras: no
lights: no
custom extras: no unless a later contract explicitly introduces them
```

## Runtime contract

The runtime may:

- load and clone the scene;
- position the zone at its declared anchor;
- enable/disable visual quality tiers;
- dispose resources when a zone is permanently unloaded.

The runtime must not:

- infer walkable bounds from mesh bounds;
- derive interaction stations from object names;
- treat Blender text/labels as resume content authority;
- require a GLB to render conventional HTML routes;
- silently ignore asset budget failures.

## Failure behavior

If one district asset fails:

1. do not alter world navigation authority;
2. preserve the existing certified decorative fallback until replacement is certified;
3. log/report the asset failure without leaking private data;
4. keep direct portfolio routes usable.

## Verification

Before runtime integration:

```bash
npm run art:blender
npm run art:verify
```

After integration, the full repository verification, browser matrix and performance checks are required by the Blender workflow certification contract.
