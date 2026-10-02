# Command Center camera composition

Status: accepted by explicit user approval on 2026-10-02.

The first authored preview cropped the hero and excluded the rear skyline.
The user approved a synchronized composition direction after the camera study:

- Blender preview position `(0, -21, 10)`, target `(0, 0, 1.6)`, FOV 52 degrees.
- Future runtime equivalent position `[0, 10, 21]`, target `[0, 1.6, 0]`.

This supersedes the initial preview position/target in the Stage 02 authoring
specification. Bootstrap and preview share these constants. Existing authored
source receives the same camera transform before its next preview.

This milestone changes preview composition only. Runtime CameraRig and React
remain unchanged; implementing the approved runtime direction belongs to the
later explicit visual acceptance/integration gate. Movement, stations, bounds,
clearances and topology remain authoritative and unchanged.
