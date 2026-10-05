# Local Blender Command Center lane

This directory is the local creative-authoring lane for Stage 02.

## What lives here

```text
art/blender/command-center/
  source/
    command-center.blend
  references/
    README.md
    command-center-concept.png
  previews/
    runtime.png
  validation.json
```

The production browser asset remains:

`public/world/art/command-center.glb`

## Important distinction

The Stage 01 GLB was generated procedurally by headless Blender on GitHub Actions. It proves the Blender/export path only.

Stage 02 is different: local Blender GUI/source authoring is the creative source of truth.

## Local workflow

From the repository root, with Blender 4.5 LTS on PATH:

```bash
npm run art:cc:bootstrap
```

This creates a guide-only `command-center.blend` containing:

- certified bounds;
- bridge opening guides;
- spawn/Ask keep-clear guides;
- runtime-matched preview camera;
- preview-only lights;
- export/guide/preview collection structure.

Then open:

`art/blender/command-center/source/command-center.blend`

Model only production art under:

`EXPORT_COMMAND_CENTER`

Do not delete or move the guide markers to make the art fit.

After authoring:

```bash
npm run art:cc:validate
npm run art:cc:preview
npm run art:cc:export
npm run art:verify
```

Review `previews/runtime.png` before integrating the GLB.

## Authority

The full dimensions, clearances, naming, material palette, preview camera and acceptance criteria are in:

`docs/portfolio-world/COMMAND-CENTER-BLENDER-SPEC.md`