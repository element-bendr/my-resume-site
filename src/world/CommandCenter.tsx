import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import { Group } from "three";
import { InteractionStation } from "./InteractionStation";
import type { OptionalVectorRef } from "./WorldEntry";
import { CommandCenterArt } from "./art/CommandCenterArt";
import {
  stationsForZone,
  type StationConfig,
  type StationId,
} from "./world-config";

interface CommandCenterProps {
  movementTarget: OptionalVectorRef;
  nearbyStation: StationId | null;
  onSelectStation: (station: StationConfig) => void;
}

function MoveTargetMarker({ movementTarget }: { movementTarget: OptionalVectorRef }) {
  const marker = useRef<Group>(null);

  useFrame((state) => {
    const target = movementTarget.current;
    if (!marker.current) return;
    marker.current.visible = Boolean(target);
    if (!target) return;
    marker.current.position.set(target.x, 0.04, target.z);
    marker.current.rotation.y = state.clock.elapsedTime * 0.8;
  });

  return (
    <group ref={marker} visible={false}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.28, 0.025, 8, 24]} />
        <meshBasicMaterial color="#63d8ff" transparent opacity={0.8} />
      </mesh>
    </group>
  );
}

export function CommandCenter({
  movementTarget,
  nearbyStation,
  onSelectStation,
}: CommandCenterProps) {
  const commandStations = stationsForZone("command-center");

  return (
    <>
      <fog attach="fog" args={["#050b15", 18, 52]} />
      <ambientLight intensity={0.72} />
      <directionalLight position={[5, 9, 5]} intensity={1.25} color="#cceaff" />
      <pointLight position={[0, 4, -1]} intensity={20} distance={12} color="#58d7ff" />
      <pointLight position={[5, 2.5, -3]} intensity={8} distance={7} color="#75f2c8" />

      <CommandCenterArt />

      {commandStations.map((station) => (
        <InteractionStation
          key={station.id}
          station={station}
          nearby={nearbyStation === station.id}
          onSelect={() => onSelectStation(station)}
        />
      ))}

      <MoveTargetMarker movementTarget={movementTarget} />
    </>
  );
}
