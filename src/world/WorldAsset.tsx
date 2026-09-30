import { useGLTF } from "@react-three/drei";
import { useMemo } from "react";
import type { Group } from "three";

export function WorldAsset({ path, position, scale = 1 }: { path: string; position: [number, number, number]; scale?: number }) {
  const { scene } = useGLTF(path, false, false);
  const instance = useMemo(() => scene.clone(true) as Group, [scene]);
  return <primitive object={instance} position={position} scale={scale} />;
}

useGLTF.preload("/world/assets/v2/quaternius/Column_Astra.gltf", false, false);
