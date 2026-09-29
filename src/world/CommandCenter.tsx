import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import { Group } from "three";
import { InteractionStation } from "./InteractionStation";
import type { OptionalVectorRef } from "./WorldEntry";
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

function CoreHologram() {
  const ring = useRef<Group>(null);

  useFrame((_, delta) => {
    if (ring.current) ring.current.rotation.y += delta * 0.35;
  });

  return (
    <group position={[0, 0, 0.95]}>
      <mesh position={[0, 0.09, 0]}>
        <cylinderGeometry args={[1.25, 1.5, 0.16, 32]} />
        <meshStandardMaterial
          color="#132943"
          emissive="#07182a"
          emissiveIntensity={0.45}
          metalness={0.58}
          roughness={0.34}
        />
      </mesh>
      <group ref={ring} position={[0, 1.82, 0]}>
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[0.95, 0.035, 12, 48]} />
          <meshStandardMaterial color="#58d7ff" emissive="#1f94bd" emissiveIntensity={1.4} />
        </mesh>
        <mesh rotation={[0, Math.PI / 2, Math.PI / 4]}>
          <torusGeometry args={[0.7, 0.025, 10, 40]} />
          <meshStandardMaterial color="#9a8cff" emissive="#6957c6" emissiveIntensity={1.2} />
        </mesh>
        <mesh>
          <icosahedronGeometry args={[0.3, 1]} />
          <meshStandardMaterial
            color="#d9f7ff"
            emissive="#58d7ff"
            emissiveIntensity={1.8}
            wireframe
          />
        </mesh>
      </group>
    </group>
  );
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

      <gridHelper args={[16, 16, "#173a58", "#0c2138"]} position={[0, 0.012, 0]} />
      <CoreHologram />

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
