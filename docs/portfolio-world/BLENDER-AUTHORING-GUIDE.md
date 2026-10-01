# Blender Authoring Guide

## Toolchain

Pinned authoring target:

- Blender 4.5 LTS;
- initial automated bake: Blender 4.5.14;
- glTF/GLB exporter shipped with that Blender release.

The repository generator is:

`tools/blender/generate_world.py`

## Reproducible build

From repository root:

```bash
npm ci
npm run art:blender
npm run art:verify
```

Equivalent direct invocation:

```bash
blender -b --python tools/blender/generate_world.py
```

A manual GitHub Actions bake exists at `.github/workflows/blender-assets.yml`. It is deliberately `workflow_dispatch` only so ordinary commits do not burn Actions minutes downloading Blender.

## Authoring order

For every district:

1. preserve the existing zone bounds and interaction coordinates;
2. block the major architectural silhouette;
3. establish large/medium/small shape hierarchy;
4. bevel hero edges and smooth curved forms;
5. add visual anchors corresponding to the district purpose;
6. add restrained emissive accents;
7. export;
8. check asset budget;
9. inspect in the production camera, not just Blender's viewport;
10. only then add texture detail.

## Visual language

Portfolio World should read as one coherent near-future environment, not six unrelated asset-store purchases.

Shared rules:

- dark architectural base;
- controlled metallic surfaces;
- rounded/beveled industrial forms;
- one principal accent per district;
- emissive light as information hierarchy, not Christmas decoration;
- readable silhouettes from the third-person camera;
- enough negative space for player movement and station overlays.

District accents remain:

- Command Center: cyan/blue;
- Build Lab: violet;
- Automation Lab: green/cyan;
- Client Street: warm orange;
- Timeline: gold;
- Hobby District: pink/magenta.

## Scene scale

Use the existing runtime zones as the size constraint. Do not enlarge a building until the player no longer fits and then “fix” navigation to match it. That is asset-led architecture, a reliable way to turn one pretty prop into six regressions.

## Lighting ownership

GLBs initially contain no exported lights.

Runtime owns:

- environment light;
- key/fill/rim lighting;
- quality-tier shadow policy;
- fog;
- post-processing.

Blender may use temporary authoring lights for preview, but they are not exported unless a later recorded decision changes this rule.

## Bakes and textures

When textures are added:

- keep original authoring sources outside runtime bundles;
- bake only what improves the shipped scene;
- use consistent texel density;
- avoid unique 2K/4K maps for small props;
- prefer packed ORM-style maps where the chosen runtime pipeline supports them;
- transcode production textures to KTX2/Basis;
- keep a source-to-output record for reproducibility.

## LOD policy

LOD is introduced only after actual asset and frame-time measurements.

Preferred order:

1. simplify unseen geometry;
2. reduce material count;
3. compress textures;
4. use instancing;
5. then add LODs for expensive hero/architectural assets.

Do not create three LOD variants of an object that was only 200 triangles to begin with. Software has enough ceremonial complexity already.

## Source-control policy

Textual/procedural Blender generation belongs in Git.

If hand-authored `.blend` files are later required:

- keep them in a clearly named source directory;
- document Blender version;
- avoid embedding unnecessary render caches;
- do not place large transient bakes in Git history;
- consider Git LFS only after measuring actual source-file size and collaboration needs.

Production GLBs may be committed only after their deterministic/source provenance and asset budget are recorded.

## Review evidence

For each integrated zone retain:

- source generator or source file;
- exact GLB hash;
- byte size;
- triangle/material/texture counts when tooling is added;
- desktop screenshot;
- mobile screenshot;
- frame-time/FPS sample;
- runtime console/network result;
- rollback/fallback result;
- validated commit.
