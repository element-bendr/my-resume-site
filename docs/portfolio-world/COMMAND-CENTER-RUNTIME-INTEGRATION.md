# Command Center runtime integration

Status: bounded candidate for `command-center-runtime-001`.

## Boundary

`CommandCenterArt` loads `/world/art/command-center.glb` only through
`BLENDER_ART_ASSETS["command-center"]` and places it only through
`BLENDER_ART_PLACEMENTS["command-center"]`. The GLB is decorative scenery;
React remains authoritative for topology, movement, camera, stations, Ask
content, and navigation.

The accepted export is preserved byte-for-byte:

| Artifact | SHA-256 | Size |
| --- | --- | ---: |
| `public/world/art/command-center.glb` | `72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496` | 845512 bytes |

## Failure behavior

The authored scene is behind `Suspense` and a local class error boundary.
While loading or if the GLB fails, a small decorative pedestal renders and
the rest of the world remains available. The conventional route and the
outer WebGL fallback are unchanged.

## Preserved runtime authority

`CommandCenter` still renders the existing fog, lights, `InteractionStation`,
and `MoveTargetMarker`. The duplicate procedural grid and core hologram were
removed; no station, spawn, bridge, camera, content, or navigation data comes
from GLB meshes or object names. Other districts retain their existing lazy
loading path.
