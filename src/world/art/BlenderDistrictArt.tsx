import { useGLTF } from "@react-three/drei";
import type { ZoneId } from "../world-topology";

export const BLENDER_ART_ASSETS: Record<ZoneId, string> = {
  "command-center": "/world/art/command-center.glb",
  "build-lab": "/world/art/build-lab.glb",
  "automation-lab": "/world/art/automation-lab.glb",
  "client-street": "/world/art/client-street.glb",
  timeline: "/world/art/timeline.glb",
  "hobby-district": "/world/art/hobby-district.glb",
};

export const BLENDER_ART_PLACEMENTS: Record<
  ZoneId,
  readonly [number, number, number]
> = {
  "command-center": [0, 0, 0],
  "build-lab": [-9, 0, -16],
  "automation-lab": [9, 0, -16],
  "client-street": [-17, 0, 0],
  timeline: [0, 0, 17],
  "hobby-district": [17, 0, 0],
};

interface BlenderDistrictArtProps {
  zoneId: ZoneId;
  position?: readonly [number, number, number];
  rotation?: readonly [number, number, number];
}

export function BlenderDistrictArt({
  zoneId,
  position = BLENDER_ART_PLACEMENTS[zoneId],
  rotation = [0, 0, 0],
}: BlenderDistrictArtProps) {
  const { scene } = useGLTF(BLENDER_ART_ASSETS[zoneId]);

  return (
    <group position={position} rotation={rotation}>
      <primitive object={scene.clone(true)} />
    </group>
  );
}

export function preloadBlenderDistrict(zoneId: ZoneId) {
  useGLTF.preload(BLENDER_ART_ASSETS[zoneId]);
}
