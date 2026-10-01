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

interface BlenderDistrictArtProps {
  zoneId: ZoneId;
  position?: readonly [number, number, number];
  rotation?: readonly [number, number, number];
}

export function BlenderDistrictArt({
  zoneId,
  position = [0, 0, 0],
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
