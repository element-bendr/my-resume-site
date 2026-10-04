import { Component, Suspense, type ReactNode } from "react";
import { useGLTF } from "@react-three/drei";
import {
  BLENDER_ART_ASSETS,
  BLENDER_ART_PLACEMENTS,
} from "./blender-art-config";

export const COMMAND_CENTER_ART_ASSET = BLENDER_ART_ASSETS["command-center"];
export const COMMAND_CENTER_ART_PLACEMENT = BLENDER_ART_PLACEMENTS["command-center"];

function CommandCenterArtFallback() {
  return (
    <group position={BLENDER_ART_PLACEMENTS["command-center"]}>
      <mesh position={[0, 0.08, 0]}>
        <cylinderGeometry args={[1.3, 1.5, 0.16, 24]} />
        <meshStandardMaterial
          color="#132943"
          emissive="#07182a"
          emissiveIntensity={0.45}
          metalness={0.58}
          roughness={0.34}
        />
      </mesh>
    </group>
  );
}

class CommandCenterArtBoundary extends Component<
  { children: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error: Error) {
    console.error("Command Center scenery failed to load.", error);
  }

  render() {
    return this.state.failed ? <CommandCenterArtFallback /> : this.props.children;
  }
}

function CommandCenterArtScene() {
  const { scene } = useGLTF(COMMAND_CENTER_ART_ASSET);

  return (
    <group position={COMMAND_CENTER_ART_PLACEMENT}>
      <primitive object={scene.clone(true)} />
    </group>
  );
}

export function CommandCenterArt() {
  return (
    <CommandCenterArtBoundary>
      <Suspense fallback={<CommandCenterArtFallback />}>
        <CommandCenterArtScene />
      </Suspense>
    </CommandCenterArtBoundary>
  );
}
