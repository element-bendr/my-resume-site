# Portfolio World — Canonical Visual Reference Contract

## Visual authority

The canonical visual authority for the 3D world is the **approved generated floating-world reference from the controlling project conversation**.

This document translates that approved image into implementation constraints. Current screenshots, procedural blockouts, asset-pack examples, and library defaults are evidence only. They must not override the reference.

If implementation convenience conflicts with the reference, the implementation must change.

## Core composition

The spawn view must read immediately as a premium stylized floating sci-fi world.

Required spatial hierarchy:

1. a dominant Central Plaza / Command Center in the foreground-midground;
2. the player grounded in the lower third of frame;
3. a strong central holographic/system landmark;
4. multiple elevated architectural masses framing the plaza;
5. bridges visibly connecting outward;
6. at least three destination silhouettes visible from spawn;
7. layered depth: foreground player/props, midground plaza/architecture, background districts/skyline;
8. visible floating-island separation and atmospheric void/depth beneath or around the platforms.

The scene must not read as a single dark slab viewed from above.

## Camera composition

Target presentation from the approved reference:

- elevated third-person 3/4 view, not top-down;
- approximate camera height: 4–6 world units;
- approximate camera distance behind player: 6–9 world units;
- pitch: roughly 35–50 degrees downward;
- FOV: roughly 45–55 degrees;
- player in lower third;
- horizon and destination architecture visible;
- Central Plaza occupies the middle of the frame;
- camera should reveal the world ahead rather than maximize visible floor area.

Movement/input behavior remains protected. Camera tuning is visual composition work only.

## Central Plaza

The reference depicts a designed architectural place, not a platform.

Required:
- layered circular or radial plaza;
- steps, ramps, retaining walls or level changes;
- real architectural towers/façades around the hub;
- slimmer structural framing rather than four dominant black pillars;
- central holographic globe/system core;
- planter beds / vegetation;
- benches / street furniture / terminals;
- railings and bridge mouths;
- readable pedestrian scale;
- cool cyan system accents with warm environmental lighting.

The hologram is a landmark, not the entire scene. It should generally occupy less than roughly one quarter of the vertical frame.

## Floating-world structure

The world should visibly read as connected floating districts.

Required:
- Central Plaza as primary island/hub;
- bridges extending toward district islands;
- district silhouettes visible from the hub;
- atmospheric depth beneath/behind platforms;
- island edges and underside masses that feel intentional, not arbitrary polygon cones;
- distant architectural forms, skyline silhouettes, or terrain masses to prevent an empty void.

## Architecture

Visible hero architecture must be asset-driven.

Target:
- at least 70–80% of visible Central Plaza architecture should come from curated GLTF environment assets or deliberately authored equivalent geometry;
- procedural primitives are allowed for collision, invisible navigation, holograms, simple trims, effects, island undersides, and minor glue geometry;
- obvious placeholder boxes, giant black prisms, and debug-like slabs are not acceptable in the hero composition.

Architecture should provide:
- vertical scale;
- recognizable entrances;
- façade rhythm;
- structural framing;
- windows/panels;
- stairs/platform changes;
- believable bridge supports;
- a skyline readable at a glance.

## Material language

Base palette:
- pale architectural stone / warm concrete;
- charcoal/brushed metal;
- restrained glass;
- muted vegetation;
- cyan system lighting;
- warm sunset highlights.

Approximate visual balance:
- 50–60% neutral architecture;
- 15–25% landscape / vegetation;
- 10–20% metal / glass detail;
- 5–10% emissive signage and accents.

Avoid a scene dominated by dark grey/black surfaces and cyan emission.

## Lighting and atmosphere

Reference mood:
- sunset / blue-hour;
- warm directional sun/key;
- cool hemisphere/environment fill;
- visible sky gradient;
- restrained fog for depth;
- coherent shadows/contact depth;
- subtle practical lights and emissive signage;
- restrained bloom only after base lighting/material response reads correctly.

The environment should remain readable without relying on neon emission.

## Player

The player must:
- be clearly readable against the environment;
- appear grounded at believable human scale;
- remain in the lower third of the spawn frame;
- not dominate the architecture;
- use the existing certified movement system.

A proper low-poly humanoid GLB is preferred when budget-safe. The procedural avatar may remain temporarily as fallback.

## District identities visible from the hub

The reference establishes distinct destination identities.

- Build Lab: violet technical/industrial accent.
- Automation Lab: emerald/cyan operations accent.
- Client Street: warm amber/commercial accent.
- Timeline Corridor: blue/gold archive accent.
- Hobby District: magenta/playful garden-studio accent.

These are accent systems, not full-scene color washes.

## Vegetation and human scale

The hero frame must contain visible environmental scale cues such as:
- trees or shrubs;
- planters;
- benches;
- lamps;
- railings;
- signs;
- terminals;
- small props.

Without these cues, the scene reads as abstract geometry rather than a place.

## Bridge requirement

At least one bridge in the spawn composition must read as a finished architectural object:
- deck;
- railings;
- structural supports;
- emissive/navigation accents;
- visual connection toward a destination silhouette.

A plain rectangular strip is insufficient.

## Reference-match acceptance gate

The hero screenshot at 1440px must visibly demonstrate all of the following:

- player in lower third;
- visible horizon/sky;
- Central Plaza reads as architecture, not a slab;
- central hologram is proportionate;
- at least three district silhouettes visible;
- at least one finished bridge visible;
- vertical architectural layering visible;
- vegetation/scale props visible;
- warm/cool lighting contrast visible;
- majority of hero architecture is asset-driven;
- no dominant placeholder pillars/boxes;
- no large empty floor region dominating the frame;
- no runtime errors or failed asset requests.

A technically green build does **not** pass this gate by itself.

## User visual authority

The final hero scene requires explicit user visual acceptance against the approved reference before district production continues.

Terra validates technical integrity and protected state. Terra does not substitute for visual acceptance.

## Protected state

Do not change:
- movement math/constants;
- movement input semantics;
- topology graph/bounds;
- fast-travel behavior;
- station IDs or interaction points;
- Ask/content/routes;
- conventional fallback behavior;
- production deployment;
- main.

## Stop rule

If a hero candidate remains compositionally closer to the rejected blockout than to the approved reference, stop and revise the hero scene. Do not propagate that style to the remaining districts.
