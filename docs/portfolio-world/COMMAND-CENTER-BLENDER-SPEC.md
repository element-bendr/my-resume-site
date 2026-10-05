# Command Center Blender Authoring Specification

status: FROZEN_FOR_STAGE_02_AUTHORING
scope: Command Center only
runtime zone: `command-center`

## 1. Authority

This specification converts the certified runtime constraints into a Blender authoring brief.

Existing runtime facts are authoritative where cited below. New dimensional and visual values in this file are **Stage 02 design constraints** chosen to make the art reproducible. They may be changed only through an explicit Stage 02 contract update before visual acceptance.

The previously generated concept image is not currently committed to this repository. Therefore this specification is the canonical build brief until a reference image is added under:

`art/blender/command-center/references/command-center-concept.png`

A future reference image may refine styling, but it may not override the protected movement, station, camera or clearance constraints in this file.

## 2. Certified runtime envelope

Runtime coordinates:

- X: left/right
- Y: up
- Z: depth

Command Center bounds:

- X: `-8.0 .. +8.0`
- Z: `-6.0 .. +6.0`
- authored anchor: `[0, 0, 0]`

Local Blender mapping:

```text
runtime X -> Blender X
runtime Z -> Blender -Y
runtime Y -> Blender Z
```

Do not move runtime topology to compensate for art.

## 3. Protected runtime points

### Player spawn

Runtime:

`{ x: 0.0, z: 3.5 }`

Blender ground-plane point:

`(X=0.0, Y=-3.5)`

### Ask Terminal

Station position:

`[4.35, 0, -2.70]`

Blender ground-plane point:

`(X=4.35, Y=2.70)`

Interaction point:

`{ x: 3.55, z: -1.45 }`

Blender ground-plane point:

`(X=3.55, Y=1.45)`

Interaction radius remains runtime-owned at `1.45`.

## 4. Five protected entrances

The Command Center must visually connect to all existing bridges.

| Entrance | Runtime edge | Required clear opening |
| --- | --- | --- |
| Client Street | west | X `-8.0 .. -5.8`, Z `-1.6 .. +1.6` |
| Hobby District | east | X `+5.8 .. +8.0`, Z `-1.6 .. +1.6` |
| Timeline | north / +Z | X `-1.6 .. +1.6`, Z `+3.8 .. +6.0` |
| Build Lab | south-west / -Z | X `-6.5 .. -3.5`, Z `-6.0 .. -3.8` |
| Automation Lab | south-east / -Z | X `+3.5 .. +6.5`, Z `-6.0 .. -3.8` |

No wall, console, pylon, decorative prop or low arch may occupy these openings between runtime heights `0.35 .. 2.15`.

Overhead structure may cross a protected opening only when its underside remains at least `2.25` runtime units above the floor.

## 5. Additional keep-clear regions

### Spawn clearance

Keep clear from solid vertical scenery:

- X `-1.30 .. +1.30`
- Z `+2.20 .. +4.80`
- runtime height `0.35 .. 2.15`

### Ask approach

Keep clear from solid vertical scenery:

- X `+2.70 .. +5.10`
- Z `-3.50 .. -0.50`
- runtime height `0.35 .. 2.15`

The Ask Terminal itself remains a React interaction object. Blender may frame it architecturally but must not replace it or visually hide its label.

### Main circulation annulus

The primary walk loop is the radial band between:

- inner radius: `1.75`
- outer radius: `4.70`

Solid scenery that occupies player height must not sit inside this annulus.

Allowed inside the annulus:

- floor inlays <= `0.20` high;
- recessed emissive strips;
- overhead arches with underside >= `2.25`;
- transparent/non-blocking decorative effects that do not steal pointer events.

This deliberately leaves the central hero core and perimeter architecture as the two main massing zones.

## 6. Command Center architectural composition

The room should read as a **premium near-future operations hub**, not a room assembled from visible default cubes.

### A. Floor shell

Target:

- footprint: approximately `15.6 x 11.6`
- maximum floor-shell thickness: `0.20`
- outer corners: visibly rounded/chamfered
- five entrance cuts aligned to the protected bridge openings
- at least three radial/concentric floor bands
- recessed emissive guidance strips rather than raised barriers

Required object family:

`cc_floor_*`

### B. Central command dais

Target:

- total radius: `1.55 .. 1.65`
- base height: `0.12 .. 0.20`
- second tier radius: `1.15 .. 1.30`
- second tier total height: <= `0.32`
- curved/chamfered edge treatment
- no full-height obstruction extending into the circulation annulus

Required object:

`cc_core_dais`

### C. Hero holographic core

Visual purpose: first focal point when entering the world.

Target envelope:

- visible core radius: `0.45 .. 0.70`
- ring radius: `0.85 .. 1.15`
- top height: `2.5 .. 3.1`
- minimum three layers: physical base, luminous core, orbital/ring structure
- asymmetry/overlap is encouraged; a single torus over a cylinder is not sufficient

Required object family:

`cc_core_*`

### D. Perimeter architectural shell

Use the outer band beyond radius approximately `4.8`.

Include:

- segmented curved wall/buttress language;
- inset wall panels;
- five portal frames corresponding to the five exits;
- layered ceiling/rib silhouettes;
- negative-space breaks rather than one continuous box wall.

Target wall/pylon height:

`2.4 .. 4.8`

Maximum authored height without explicit review:

`5.2`

Required object families:

`cc_shell_*`
`cc_pylon_*`
`cc_portal_*`

### E. Structural ribs / arches

Use curved or faceted structural ribs to give the Command Center vertical identity.

Requirements:

- five primary directions should visually acknowledge the five exits;
- underside over walk areas >= `2.25`;
- use repeated source geometry/linked duplicates where appropriate;
- avoid a perfect cage around the player;
- preserve camera sightline to the central core.

Required objects:

`cc_arch_client`
`cc_arch_hobby`
`cc_arch_timeline`
`cc_arch_build`
`cc_arch_automation`

### F. Perimeter consoles

Target:

- inner edge radius >= `4.75`
- working height approximately `0.85 .. 1.25`
- tilted/recessed display surfaces;
- grouped into 3–5 visual clusters;
- no cluster may occupy a protected entrance or Ask approach.

Required object family:

`cc_console_*`

### G. Ask Terminal frame

The React Ask Terminal stays at its certified position. Blender supplies only environmental framing.

Suggested composition:

- curved canopy/backplate behind the station;
- teal/cyan accent distinct from the core;
- no solid geometry between the interaction point and the station;
- top canopy may overhang if underside >= `2.25`.

Required object:

`cc_ask_frame`

## 7. Shape-language rules

Required:

- rounded/chamfered hard-surface edges;
- layered surfaces with visible depth;
- curved or faceted structural forms;
- inset panels instead of stickers on flat walls;
- repeated geometry uses linked data/instances while authoring;
- silhouette must remain legible from the runtime camera.

Avoid:

- unmodified cubes as finished hero geometry;
- long featureless rectangular walls;
- razor-sharp 90-degree hero edges;
- random greebles at equal density everywhere;
- dense pipes/cables that turn the scene into visual noise;
- geometry whose only purpose is to imitate detail visible in a texture.

## 8. Material system

Use no more than 10 production materials for the Command Center in Stage 02.

### CC_Graphite

- base: `#07111F`
- metallic: `0.45 .. 0.60`
- roughness: `0.30 .. 0.42`
- use: primary architectural shell

### CC_Gunmetal

- base: `#13263A`
- metallic: `0.65 .. 0.80`
- roughness: `0.22 .. 0.34`
- use: frames, ribs, mechanical layers

### CC_SoftMetal

- base: `#7892A5`
- metallic: `0.35 .. 0.55`
- roughness: `0.30 .. 0.45`
- use: edge highlights and secondary panels

### CC_Cyan

- visible accent: `#58D7FF`
- emissive accent
- use: core, portal guidance, selected panel channels

### CC_Teal

- visible accent: `#75F2C8`
- use: Ask framing and secondary systems

### CC_Violet

- visible accent: `#9A8CFF`
- use: no more than roughly 10% of luminous accents
- purpose: depth separation, not a second dominant palette

### CC_DarkGlass

- base tint: `#0B2535`
- roughness: `0.08 .. 0.20`
- metallic: <= `0.10`
- transparency/transmission only if the exported GLB and runtime test remain stable

Texture images are optional for Stage 02. Geometry/material design must already read well without depending on 4K textures.

## 9. Detail hierarchy

### Large forms

Must carry the composition from a distance:

- floor shell;
- core/dais;
- perimeter shell;
- five portal frames;
- primary arches/ribs.

### Medium forms

Visible during normal third-person exploration:

- console banks;
- layered wall recesses;
- canopy/frame around Ask;
- floor tracks;
- pylon panel breaks.

### Small forms

Use sparingly:

- vents;
- seams;
- fasteners;
- thin luminous channels;
- small display recesses.

If small detail does not survive the runtime camera, bake it or delete it.

## 10. Geometry and material budget

Stage 02 target for the authored Command Center:

- triangles: `35,000 .. 90,000` preferred
- soft ceiling: `120,000` triangles before an explicit performance review
- production materials: <= `10`
- image textures: preferably <= `6`
- normal texture: <= `512 KiB` each after production compression
- exceptional hero texture: <= `1 MiB`
- production Command Center GLB: target <= `4 MiB`

Do not spend the entire polygon budget because Blender offers polygons free of emotional consequence.

## 11. Canonical preview camera

The principal Blender preview uses the user-approved camera composition in
`decisions/2026-10-02-command-center-camera-composition.md`. Runtime adoption is
deferred until visual acceptance and integration; existing CameraRig is unchanged.

Runtime:

- approved future camera position: `[0, 10, 21]`
- approved future target: `[0, 1.6, 0]`
- field of view: `52°`

Blender:

- camera position: `(0, -21, 10)`
- target point: `(0, 0, 1.6)`
- FOV: `52°`

Name:

`PREVIEW_RUNTIME`

Preview render:

- 1600 x 900
- Eevee Next
- AgX
- exposure 0
- opaque background `#050B15`

Additional review views may be added, but they do not replace `PREVIEW_RUNTIME`.

## 12. Preview-only lighting

Preview lighting is not exported.

Match the current runtime lighting approximately:

- cool key/sun from Blender `(5, -5, 9)`;
- cyan point near Blender `(0, 1, 4)`;
- teal point near Blender `(5, 3, 2.5)`;
- dim world/environment fill.

All preview lights belong under:

`PREVIEW_DO_NOT_EXPORT`

## 13. Blender collection contract

Required top-level collections:

```text
EXPORT_COMMAND_CENTER
GUIDES_DO_NOT_EXPORT
PREVIEW_DO_NOT_EXPORT
```

Only objects under `EXPORT_COMMAND_CENTER` are eligible for production export.

Guide objects and preview cameras/lights must never enter the GLB.

## 14. File contract

Authoring source:

`art/blender/command-center/source/command-center.blend`

Reference directory:

`art/blender/command-center/references/`

Preview output:

`art/blender/command-center/previews/runtime.png`

Production export:

`public/world/art/command-center.glb`

Validation report:

`art/blender/command-center/validation.json`

## 15. Visual acceptance

Stage 02 visual review fails if any of these remain true:

- the scene reads primarily as boxes/cylinders/toruses;
- the central core is just the Stage 01 procedural blockout with more bevels;
- five exits are not visually legible;
- wall/rib hierarchy has no meaningful depth;
- silhouettes collapse into flat rectangles from `PREVIEW_RUNTIME`;
- the Ask Terminal is visually buried;
- the player spawn looks obstructed;
- architecture clips into the protected walk lanes;
- emissive material dominates the solid architecture;
- the result could plausibly be reproduced faster in raw R3F primitives than in Blender.

A PASS requires:

- clear authored architectural silhouette;
- large/medium/small detail hierarchy;
- curved/chamfered form language;
- central hero focus;
- five readable portal directions;
- preserved movement clearances;
- coherent PBR palette;
- satisfactory canonical preview render;
- source validation PASS;
- GLB structural/budget PASS.

## 16. Runtime acceptance after visual PASS

Only after the authored Blender render passes:

1. export `command-center.glb`;
2. run source validator;
3. run `npm run art:verify`;
4. integrate GLB into the Command Center;
5. keep visual meshes from stealing pointer events;
6. test keyboard/click/tap movement;
7. test Ask interaction;
8. test five exits/fast travel;
9. test route teardown;
10. test 360/390/768/1024/1440 viewports;
11. record exact `.blend` SHA, GLB SHA, preview and candidate commit.
