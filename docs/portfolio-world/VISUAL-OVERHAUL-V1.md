# Portfolio World Visual Overhaul v1

## Visual north star

The world should read as a premium stylized sci-fi diorama: a central elevated Command Center connected by luminous bridges to distinct floating districts. The generated concept approved in the controlling conversation is the art-direction reference.

Translate the reference into browser-safe WebGL rather than reproducing photorealistic concept-art density.

## Preserve

- current movement speeds, acceleration, keyboard/click/tap controls;
- current camera interaction contract;
- semantic hub-and-spoke topology;
- station positions and interaction points unless later visual QA proves a local obstruction;
- map fast travel;
- lazy district loading;
- conventional routes and no-WebGL fallback;
- Ask behavior and grounded content;
- accessibility, reduced-motion and touch-target behavior;
- existing asset budgets.

## Visual language

### Global
- sunset / blue-hour sky with warm sun and cool ambient fill;
- floating architectural islands above atmospheric depth;
- pale stone / charcoal metal as base materials;
- cyan as shared navigation/system light;
- district colors used as accents rather than full-scene washes;
- strong silhouettes, vertical towers, bridges and visible destinations;
- planted greenery to soften hard sci-fi geometry;
- subtle emissive trims and holograms, never full-screen bloom soup.

### Command Center
- strongest visual landmark;
- concentric plaza tiers;
- central holographic globe/system core;
- four architectural pylons framing the plaza;
- visible bridge mouths toward all districts;
- identity plaque / system hub feeling.

### Build Lab
- violet technical workshop;
- cranes, benches, modular bays, prototype displays;
- industrial framing with warm practical lights.

### Automation Lab
- emerald/cyan operations facility;
- server/data towers, pipeline rails, node visualizations;
- precise machine-room composition.

### Client Street
- warm amber storefront architecture;
- glass-like project façades, signage, landscaped walkway;
- each client should read as a place rather than a pedestal.

### Timeline Corridor
- elevated archive / promenade;
- chronological pylons and milestone frames;
- gold/blue lighting and long sightline.

### Hobby District
- playful magenta quarter;
- garden / arcade / studio language;
- gaming, anime, fitness, philosophy and tinkering represented as themed corners.

## Rendering strategy

Use existing Three.js / React Three Fiber / Drei / WebGL 2 stack.

Prefer:
- procedural/modular geometry for the first pass;
- shared materials;
- baked/static appearance where possible;
- one global sun/key light plus ambient/hemisphere fill;
- limited district-local practical lights;
- ACES filmic tone mapping;
- fog/atmospheric depth;
- lazy district art.

Avoid:
- per-object dynamic lights;
- real-time mirror reflections;
- large crowds;
- unique 4K textures;
- mandatory WebGPU;
- movement or navigation changes disguised as visual work.

## First implementation slice

1. global sky, fog, key/fill lighting and filmic tone mapping;
2. floating-island foundations beneath all semantic zones;
3. architectural bridge dressing while retaining existing walkable bridge surfaces;
4. Command Center hero-art pass;
5. replace the placeholder primitive avatar with a recognizable stylized player while leaving controller math unchanged;
6. validate build/tests/budgets and inspect the hero scene before district-detail passes.

## Acceptance for this slice

- movement/navigation tests remain unchanged and pass;
- no station or destination becomes unreachable;
- WorldTopology semantic bounds remain unchanged;
- conventional routes remain independent of world runtime;
- no-WebGL fallback remains valid;
- reduced-motion behavior remains valid;
- initial and world asset budgets remain within frozen thresholds;
- visual inspection clearly shows a floating-world composition, Central Plaza landmark, bridges and a recognizable player;
- no production deployment from this branch.
