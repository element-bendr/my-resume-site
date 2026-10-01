# Blender art-direction upgrade

Status: **IMPLEMENTATION STARTED — asset-authoring lane**

## Goal

Replace the current primitive-heavy visual scenery with Blender-authored GLB assets while preserving
the certified world controls and application behavior.

The generated concept image remains the art-direction target. The existing Three.js world remains the
interaction/collision contract.

## Non-negotiable preserved behavior

- world bounds, bridges and zone topology
- keyboard/click movement and fast travel
- camera rig
- interaction station coordinates and content
- lazy district loading
- route isolation
- Ask Terminal behavior
- accessibility/focus contracts
- no-WebGL fallback
- Cloudflare deployment model

## Pipeline

```text
concept/reference
      ↓
Blender 4.5 LTS
      ↓
authored geometry + PBR materials
      ↓
GLB per district
      ↓
asset budget gate
      ↓
R3F BlenderDistrictArt
      ↓
district-by-district visual replacement
      ↓
visual + performance certification
```

## Initial asset budget

- six GLBs
- <= 900 KiB per district for the untextured first pass
- <= 4 MiB total GLB payload
- no textures in pass 1
- later textures must use KTX2/Basis and explicit mobile LODs

## First-pass visual language

Command Center: circular layered dais, holographic rings, radial consoles, illuminated pylons.

Build Lab: beveled archive wall, review chamber, framed display bays, purple-violet emissive trim.

Automation Lab: agent pods, linked data rails, runtime wall and green-cyan emissive nodes.

Client Street: architectural storefront shells, glazing, awnings, lit signs, bollards and a defined street.

Timeline Corridor: continuous luminous rail, milestone pillars, plaques and crown rings.

Hobby District: rounded central stage with gaming, kettlebell, anime/display and philosophy props.

## Promotion sequence

1. Generate and budget-check the six GLBs.
2. Add scenery to the Command Center only.
3. Browser QA desktop/mobile and verify no control/collision regression.
4. Replace decorative primitive scenery district by district.
5. Add lighting/post-processing only after the authored geometry is stable.
6. Add texture baking/compression and LODs.
7. Run the repository's full verification and visual QA before merge.

Main stays untouched until that chain is green.
