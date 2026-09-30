# Movement and Camera Architecture

## Design goal

Movement must make the visitor feel physically present in the portfolio without introducing game-skill requirements.

The chosen model is **guided third-person exploration**:
- elevated third-person camera;
- WASD / arrow movement on desktop;
- click-to-move on desktop;
- tap-to-move on touch devices;
- constrained walkable navigation;
- context-sensitive interaction;
- map-based fast travel;
- no jumping, combat, falling, or mandatory physics.

## Player model

The avatar is intentionally stylized and lightweight.

Required animation states:
- Idle;
- Walk;
- Interact.

Optional only when justified by a concrete interaction:
- Sit.

Not part of v1:
- jump;
- crouch;
- roll;
- climb;
- swim;
- combat;
- platforming.

## Movement state machine

```text
                 movement input
        ┌──────────────────────────┐
        │                          ▼
     ┌──────┐                  ┌──────┐
     │ IDLE │ ◄──────────────► │ WALK │
     └──┬───┘     stop         └──┬───┘
        │                          │
        │ interact                 │ interaction target
        ▼                          ▼
    ┌──────────┐              ┌──────────┐
    │ INTERACT │─────────────►│   IDLE   │
    └──────────┘    close     └──────────┘

Map navigation may temporarily enter FAST_TRAVEL.
```

Primary states:
- IDLE;
- WALK;
- INTERACT;
- FAST_TRAVEL.

Do not grow this state machine without a documented interaction need.

## Navigation model

The apparent world may contain cliffs, machinery, props, vegetation, buildings, and decorative geometry. The avatar moves only over approved walkable space represented by a navigation mesh or equivalent navigation graph.

Input pipeline:

```text
Keyboard / Pointer / Touch
          │
          ▼
   PlayerController
          │
          ▼
 NavigationController
   ├─ legal target
   ├─ path query
   ├─ route
   └─ speed
          │
          ▼
      Character
          │
          ▼
     FollowCamera
```

The visual mesh is not automatically the movement mesh.

## Desktop controls

- W / Up: forward
- S / Down: backward
- A / Left: left
- D / Right: right
- mouse/pointer: limited camera orbit
- click walkable surface: move to target
- click interactive object: route to interaction point, then interact
- E: interact with current nearby target
- M: map
- Escape: close active interface / return from interaction

A visitor must be able to use either keyboard movement or mouse-driven movement.

## Mobile controls

Mobile uses point-and-click style navigation rather than a permanent virtual joystick.

- tap walkable surface: walk there;
- tap interactive object: walk to its interaction point and interact;
- swipe: limited camera rotation;
- pinch: limited zoom where enabled;
- map: fast travel.

A virtual joystick is not part of the default design.

## Speed contract

Initial tuning targets:
- normal movement: ~3.5 m/s;
- sustained/brisk movement: up to ~5 m/s;
- scripted zone transition where appropriate: up to ~6 m/s.

Movement may accelerate gently over roughly the first second of sustained input.

There is no sprint button in v1.

Actual numbers may be tuned through playtesting, but walking must feel faster than a realism-oriented game because the goal is information discovery.

## Camera contract

Camera style:
- elevated third-person;
- 3/4 view;
- slightly behind the avatar.

Initial tuning range:
- height: ~4–6 m;
- trailing distance: ~6–9 m;
- pitch: ~35–50 degrees;
- field of view: ~45–55 degrees.

Horizontal orbit is deliberately constrained. A starting design range of roughly +/-50–70 degrees around the current orientation is acceptable.

The camera must:
- avoid clipping through major geometry;
- preserve destination visibility;
- reframe interactions;
- restore predictable orientation after interactions;
- avoid free-flight camera controls.

## Interaction positioning

Each interactive object may define:
- interaction radius;
- interaction point;
- facing direction;
- camera target;
- optional animation.

When an interaction begins:
1. navigation control resolves a legal interaction point;
2. avatar walks to that point if needed;
3. avatar faces the object;
4. movement input is suspended;
5. camera reframes;
6. the HTML interaction surface opens.

When closed:
1. HTML surface closes;
2. interaction state clears;
3. camera returns;
4. movement input resumes.

## HTML-over-3D rule

Long-form resume/project text, forms, Ask UI, contact UI, and detailed case studies render as accessible HTML overlays or normal routes.

3D text is limited to:
- short signage;
- environmental labels;
- short wayfinding markers.

Do not render substantive resume paragraphs as texture-bound or scene-bound text.

## Proximity cues

Interactive targets may use:
- glow;
- outline;
- icon;
- short label;
- E/click prompt.

Cues become prominent only within a useful interaction distance so the world does not become a field of floating tooltips.

## Zone transitions and prefetch

Connecting paths and bridges double as loading boundaries.

```text
approach connector
      │
      ├─ prefetch destination GLB
      ├─ prefetch required textures
      ├─ prefetch structured zone content
      ▼
cross connector
      │
      ▼
destination ready
```

Loading behavior must respect the asset-budget document.

## Fast travel

The Map is a first-class navigation mechanism.

Selecting a destination:
- validates that the destination is available;
- loads required assets if needed;
- moves the visitor to the destination spawn/entry point;
- settles the camera into that zone.

Default visual transition target: roughly 500–800 ms.

Reduced-motion mode should replace cinematic travel with an immediate or minimal transition.

## Guided freedom

The world looks free-roaming but intentionally guides movement with:
- light;
- paths;
- architecture;
- signage;
- visible landmarks;
- bridge orientation;
- camera framing.

The user should rarely need to consult instructions to understand where they can go.

## Failure behavior

If pathfinding fails:
- do not move the character through geometry;
- clear the invalid target;
- preserve user control;
- optionally provide a subtle destination-unavailable cue.

If the 3D controller fails entirely:
- preserve the conventional HTML portfolio/navigation path.

## Performance rules

- movement logic must not require heavyweight rigid-body physics;
- prefer deterministic kinematic/navmesh movement;
- repeated environment props should not create per-object movement costs;
- camera and animation updates should avoid unnecessary renders when idle;
- mobile/low-power mode may reduce animation detail and scene effects, never content reachability.

## Acceptance tests

Implementation must prove:
1. keyboard movement stays on legal walkable space;
2. click/tap movement resolves only legal destinations;
3. clicking an interactive object routes to its interaction point;
4. interaction locks and restores controls correctly;
5. camera returns to a predictable state after interaction;
6. map fast travel reaches every major district;
7. movement cannot leave world bounds;
8. decorative props cannot permanently trap the avatar;
9. mobile can reach every essential interaction without keyboard input;
10. reduced-motion mode removes non-essential camera travel;
11. WebGL failure still leaves Resume/Projects/Ask/Contact reachable;
12. no essential action requires jumping, combat, timing, or precision platforming.
