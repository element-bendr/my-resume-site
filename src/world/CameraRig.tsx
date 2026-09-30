import { OrbitControls } from "@react-three/drei";
import { useFrame, useThree } from "@react-three/fiber";
import type { ComponentRef } from "react";
import { useRef } from "react";
import { Vector3 } from "three";
import type { VectorRef } from "./WorldEntry";
import { CAMERA, PLAYER_SPAWN } from "./world-config";

interface CameraRigProps {
  playerPosition: VectorRef;
  reducedMotion: boolean;
}

export function CameraRig({ playerPosition, reducedMotion }: CameraRigProps) {
  const controls = useRef<ComponentRef<typeof OrbitControls>>(null);
  const camera = useThree((state) => state.camera);
  const desiredTarget = useRef(new Vector3());
  const deltaTarget = useRef(new Vector3());

  useFrame((_, delta) => {
    const instance = controls.current;
    if (!instance) return;

    desiredTarget.current.set(
      playerPosition.current.x,
      CAMERA.targetHeight,
      playerPosition.current.z,
    );
    deltaTarget.current.copy(desiredTarget.current).sub(instance.target);

    if (reducedMotion) {
      camera.position.add(deltaTarget.current);
      instance.target.copy(desiredTarget.current);
    } else {
      const factor = 1 - Math.exp(-delta * 8);
      deltaTarget.current.multiplyScalar(factor);
      camera.position.add(deltaTarget.current);
      instance.target.add(deltaTarget.current);
    }
    instance.update();
  });

  return (
    <OrbitControls
      ref={controls}
      target={[PLAYER_SPAWN.x, CAMERA.targetHeight, PLAYER_SPAWN.z]}
      enablePan={false}
      enableDamping={!reducedMotion}
      dampingFactor={0.08}
      minDistance={CAMERA.minDistance}
      maxDistance={CAMERA.maxDistance}
      minPolarAngle={CAMERA.minPolarAngle}
      maxPolarAngle={CAMERA.maxPolarAngle}
      minAzimuthAngle={-CAMERA.maxAzimuthAngle}
      maxAzimuthAngle={CAMERA.maxAzimuthAngle}
    />
  );
}
