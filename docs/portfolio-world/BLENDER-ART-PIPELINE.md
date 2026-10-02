# Blender art-direction upgrade

Status: **STAGE 01 CERTIFIED AS PIPELINE PROOF — AUTHORED ART NOT YET ACCEPTED**

## Goal

Replace the current primitive-heavy visual scenery with genuinely authored Blender scenes exported as GLB, while preserving the certified world controls and application behavior. Stage 01's procedural GLBs are pipeline-proof assets only.

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
editable Blender source + authored geometry/materials
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

1. **Pipeline proof and bake** — source/export rules, six procedurally generated GLBs, hashes/sizes. This proves export/integrity only.
2. **Command Center authored-source gate + integration** — create/obtain an editable Command Center `.blend`, visually approve it against the concept, then integrate its exported GLB.
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

Stage 01 is certified only as a procedural Blender/export pipeline proof. The six GLBs are valid runtime files but are not accepted as final visual assets. Do not replace existing scenery with them merely because they passed structural checks.
