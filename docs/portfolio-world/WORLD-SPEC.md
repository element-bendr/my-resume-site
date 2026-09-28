# Portfolio World Specification

## Purpose

This document defines the world we are building. It is a design and implementation contract, not concept art commentary.

The portfolio must feel like a compact explorable place while remaining a professional resume and project system. The visitor may explore, but must never be forced to play a game to reach evidence, projects, resume content, contact information, or the Ask interface.

## World topology

The world is a hub-and-spoke diorama connected by readable paths and bridges.

```text
                         TIMELINE CORRIDOR
                                ●
                                │
                                │
         CLIENT STREET ●──── COMMAND CENTER ────● HOBBY DISTRICT
                                │
                     ┌──────────┴──────────┐
                     │                     │
                 BUILD LAB          AUTOMATION LAB
                     │
                     ●
                ASK TERMINAL
```

The exact art layout may evolve, but the semantic topology is stable.

## Zones

### Command Center

Role:
- spawn point;
- identity and positioning;
- primary world orientation;
- primary navigation;
- system map access.

Content:
- Vijay Kumaran;
- AI Automation & Web Systems Consultant;
- Websites;
- Business Systems;
- AI Automations;
- Selected Work.

Interaction:
- central holographic/system display;
- direct links to Portfolio, Projects, Resume, Ask, Contact;
- visible paths to every major district.

### Build Lab

Role:
- production engineering and shipped systems.

Content:
- selected production systems;
- architecture/proof surfaces;
- project technologies;
- links to evidence and repositories where appropriate.

Visual language:
- machines, terminals, modular industrial systems, construction/workbench motifs.

### Automation Lab

Role:
- AI agents, infrastructure, workflows, orchestration, reliability.

Visual language:
- pipelines;
- robotic/automated machinery;
- network nodes;
- control surfaces.

The visualization must represent real system relationships rather than inventing decorative technical claims.

### Client Street

Role:
- client-facing work and shipped websites/systems.

Visual language:
- small storefronts/buildings;
- each building represents a client project or category;
- entering/inspecting opens a normal HTML project card or case study.

### Timeline Corridor

Role:
- chronological professional journey and milestones.

Visual language:
- a corridor, archive, or ascending path;
- year markers;
- milestone exhibits.

The timeline content remains derived from verified resume data.

### Hobby District

Role:
- communicate personality without contaminating professional proof.

Themes may include:
- gaming;
- anime;
- kettlebells;
- philosophy;
- tinkering/building.

This area may be more playful than the professional districts but must use the same movement and accessibility rules.

### Ask Terminal

Role:
- world representation of the existing Ask-about-the-work experience.

Interaction:
1. visitor approaches;
2. terminal highlights;
3. interact command is accepted;
4. character automatically takes the correct interaction position;
5. camera reframes;
6. HTML Ask interface opens over the 3D scene;
7. closing restores the previous camera and movement state.

The Ask system remains grounded in project evidence and is not permitted to invent resume claims.

## Visual hierarchy

The world guides without forcing.

Use:
- brighter paths;
- strong landmarks;
- lighting contrast;
- signage;
- bridges;
- environmental framing;
- visible destination silhouettes;
- limited camera composition.

Avoid:
- maze layouts;
- hidden mandatory doors;
- blind alleys;
- gameplay gates;
- collectibles required to access resume material;
- platforming or precision movement.

## Entry experience

Initial spawn:
- Command Center;
- avatar faces the primary holographic display;
- the major districts are visually legible from the starting area.

First-use help is limited to:
- WASD / arrows or click to move;
- E / click to interact;
- M / Map.

The hint disappears after basic movement/interactions and must not repeatedly obstruct the screen.

## Fast access

The global HUD always exposes:
- Map;
- Projects;
- Resume;
- Ask;
- Contact.

The 3D world is never the sole route to any essential content.

## World loading

Zones are independent lazy-load boundaries.

Approaching a connecting bridge/path begins prefetching the destination zone. The visitor should normally cross into an already-ready destination.

A zone may be unloaded or reduced after sufficient distance if memory pressure warrants it.

## Non-negotiable world invariants

1. No visitor can fall out of the world.
2. No essential content requires jumping, combat, puzzle completion, collecting items, or timing.
3. No decorative geometry may trap the avatar.
4. All professional claims originate from structured verified content.
5. Every essential 3D interaction has an HTML/direct-route equivalent.
6. Map-based fast travel can bypass normal walking.
7. The world remains understandable without audio.
8. Reduced-motion and low-power paths remain functional.
9. World geometry and media obey the repository asset budget.
10. The world must remain useful as a portfolio even if the 3D canvas cannot initialize.

## Acceptance evidence

Implementation must eventually prove:
- every zone is reachable through the navigation graph;
- every essential destination is directly reachable through HUD/map navigation;
- interaction targets can be entered and exited without state corruption;
- no navmesh route leaves legal walkable space;
- mobile navigation provides equivalent reachability;
- reduced-motion mode avoids cinematic camera travel;
- conventional routes work with WebGL disabled;
- asset-budget checks cover all shipped world assets.
