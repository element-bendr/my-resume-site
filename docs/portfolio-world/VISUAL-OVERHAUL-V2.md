# Portfolio World Visual Overhaul v2 — Asset-Based Art Production

## Canonical reference authority

The approved generated floating-world image from the controlling project conversation is the primary visual authority. `docs/portfolio-world/VISUAL-REFERENCE-CONTRACT.md` is the binding implementation translation of that image. Current screenshots, procedural blockouts, and asset-pack defaults are not design authorities and must not override it.


## Why v1 was rejected

The Stage 01 procedural visual foundation passed technical validation but failed user visual acceptance. The rendered world still reads as a dark low-poly blockout with sparse primitive geometry and weak environmental richness, materially below the approved visual reference.

Do not continue the same primitive-only construction strategy.

## Visual target

Preserve the approved floating sci-fi world composition:
- dominant Central Plaza / Command Center;
- connected floating districts;
- sunset / blue-hour atmosphere;
- strong architectural silhouettes;
- layered foreground, midground and background;
- vegetation and environmental props;
- district-specific identity through architecture, signage and accent lighting;
- readable stylized player;
- premium game-world presentation rather than debug-blockout presentation.

The target is a browser-safe stylized game environment, not a photoreal marketing render.

## New source rule

Use real modular environment assets as the primary art substrate.

Approved source classes:
- CC0 modular sci-fi architecture / props in glTF;
- CC0 city / industrial / commercial building kits in glTF;
- CC0 vegetation / street furniture / environmental props;
- custom Three.js procedural geometry only for glue geometry, holograms, trims, simple islands and effects.

Initial candidate asset sources:
- Quaternius Modular Sci-Fi MegaKit — CC0, 270+ modular pieces, glTF;
- Kenney City Kit Industrial — CC0, optimized low-poly city/factory pieces;
- Kenney City Kit Commercial — CC0, optimized low-poly commercial buildings.

Every imported asset must have its source and license recorded before merge.

## Preserve

- all existing movement math and constants;
- input behavior;
- fast travel;
- semantic topology / zone graph;
- station IDs and interaction behavior;
- Ask/content/routes;
- accessibility and fallback;
- Cloudflare Workers delivery model;
- lazy district loading.

Camera movement semantics remain protected, but the visual camera composition may be tuned for art direction so long as input behavior and reachability remain unchanged.

## Rendering stack

Remain on:
- Three.js;
- React Three Fiber;
- Drei;
- WebGL 2;
- Vite;
- Cloudflare Workers Static Assets.

Add only evidence-backed rendering helpers if needed.

## Visual production rules

### Geometry
- use modular glTF buildings/props for recognizable architecture;
- break large flat slabs with elevation changes, stairs, retaining walls, railings and layered decks;
- give each district a skyline visible from the Central Plaza;
- retain invisible/simple walkable collision geometry independent of render meshes.

### Materials
- use PBR materials from asset sources;
- favor shared atlases/materials;
- district colors appear through signage, emissive strips and practical lights, not entire surfaces;
- use KTX2/Basis only when texture payload materially benefits.

### Lighting
- one coherent sun/key light;
- hemisphere/environment fill;
- baked/static-looking scene response where possible;
- limited local practical lights;
- contact/shadow depth;
- restrained bloom only after base lighting reads correctly.

### Atmosphere
- visible sky gradient / sunset;
- fog used for depth, not concealment;
- distant silhouettes;
- vegetation and props to create scale.

### Composition
- lower, more cinematic third-person framing;
- player and destination landmarks share the frame;
- avoid near-top-down presentation except map mode;
- Central Plaza must visibly reveal multiple district destinations.

## District direction

### Central Plaza
- layered circular plaza;
- real architectural towers / façades around the hologram;
- stairs / ramps / bridges;
- planting and benches;
- holographic globe remains the dominant landmark.

### Build Lab
- industrial / workshop architecture;
- crane frames, bays, machines, workbenches;
- violet accent lighting.

### Automation Lab
- sci-fi operations architecture;
- server / node / conduit motifs;
- emerald/cyan accents.

### Client Street
- actual low-poly commercial façades;
- storefront windows, awnings, signs, street furniture;
- warm amber lighting.

### Timeline Corridor
- elevated promenade / archive;
- framed milestones integrated into architecture;
- blue/gold accents.

### Hobby District
- garden / arcade / studio mix;
- trees, neon signs, seating, small themed structures;
- magenta accents.

## Player

Keep controller math unchanged.

Visual target:
- use a proper low-poly humanoid GLB with idle/walk clips if asset budget permits;
- otherwise retain the procedural avatar only as fallback;
- player silhouette must remain readable against all districts.

## Budget

Retain frozen budgets:
- first visible 3D payload <= 3 MiB compressed;
- core first visit <= 5 MiB;
- individual GLB <= 4 MiB;
- individual lazy district pack <= 5 MiB;
- absolute internal single asset <= 10 MiB.

This requires selective asset curation, not importing entire packs.

## Stage 01 production slice

Build only:
1. Central Plaza;
2. one connecting bridge;
3. visible distant silhouettes for the five other districts;
4. proper player visual;
5. final lighting / materials / camera composition.

Do not rebuild all districts until the Central Plaza screenshot materially resembles the approved reference.

## Stage 01 acceptance

At 1440px, one screenshot from spawn must show:
- recognizable premium floating-world composition;
- Central Plaza as an architectural place, not a slab;
- at least three destination silhouettes visible;
- layered vertical architecture;
- vegetation / environmental props;
- clear warm/cool lighting;
- player visibly grounded in scene;
- no dominant primitive-blockout appearance.

User visual acceptance is required before continuing to district production.

Technical acceptance:
- typecheck/build/tests/guards/budgets PASS;
- no movement/topology/content drift;
- no runtime errors / failed requests;
- reduced motion and fallback remain valid.

## Stop rule

If the Central Plaza still reads primarily as primitive blocks after this stage, stop. Do not propagate the style to the remaining districts.
