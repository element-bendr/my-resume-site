# Blender art-direction upgrade

Status: **STAGE 01 ACTIVE — baseline asset bake not yet certified**

## Goal

Replace the current primitive-heavy visual scenery with Blender-authored GLB assets while preserving the certified world controls and application behavior.

The generated concept image remains the art-direction target. The existing React world remains the interaction, content and fallback authority.

## Documentation map

- decision: `decisions/2026-10-01-blender-world-art.md`
- asset interface: `BLENDER-ASSET-CONTRACT.md`
- modeling/export workflow: `BLENDER-AUTHORING-GUIDE.md`
- QA/certification: `BLENDER-QA-CERTIFICATION.md`
- transfer budgets: `ASSET-BUDGET.md`
- renderer policy: `RENDERING-TECHNOLOGY.md`
- active workflow: `workflow/active/portfolio-world-blender-art/`

## Non-negotiable preserved behavior

- world bounds, bridges and zone topology;
- keyboard/click/tap movement and fast travel;
- camera rig;
- interaction station coordinates and content;
- lazy district loading;
- route isolation;
- Ask Terminal behavior;
- accessibility/focus contracts;
- no-WebGL fallback;
- Cloudflare deployment model.

## Pipeline

```text
concept/reference
      ↓
Blender 4.5 LTS
      ↓
authored geometry + PBR material intent
      ↓
GLB per district
      ↓
asset budget / integrity gate
      ↓
R3F BlenderDistrictArt boundary
      ↓
Command Center vertical slice
      ↓
district-by-district replacement
      ↓
lighting / textures / post-processing
      ↓
visual + performance + accessibility certification
      ↓
reviewed merge
      ↓
separate production deployment
```

## Stage sequence

1. **Art contract and bake** — source/export rules, six GLBs, hashes/sizes.
2. **Command Center integration** — first production-camera proof.
3. **District rollout** — remaining five lazy zones.
4. **Lighting/materials/post** — quality improvements after geometry stabilizes.
5. **Performance/accessibility** — full device/runtime/fallback matrix.
6. **Certification/promotion** — exact-candidate review and controlled merge.

## First-pass visual language

Command Center: circular layered dais, holographic rings, radial consoles, illuminated pylons.

Build Lab: beveled archive wall, review chamber, framed display bays, violet emissive trim.

Automation Lab: agent pods, linked data rails, runtime wall and green-cyan emissive nodes.

Client Street: architectural storefront shells, glazing, awnings, lit signs, bollards and a defined street.

Timeline Corridor: continuous luminous rail, milestone pillars, plaques and crown rings.

Hobby District: rounded central stage with gaming, kettlebell, display/anime and philosophy props.

## Current gate

The source pipeline exists, but the binary GLBs are not yet certified.

Do not integrate or remove existing scenery until Stage 01 produces a measured six-asset candidate.
