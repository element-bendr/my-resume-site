import { useGLTF } from "@react-three/drei";
import type { ZoneId } from "../world-topology";
import {
  BLENDER_ART_ASSETS,
  BLENDER_ART_PLACEMENTS,
} from "./blender-art-config";

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
