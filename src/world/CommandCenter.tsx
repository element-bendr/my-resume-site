import type { ThreeEvent } from "@react-three/fiber";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import { Group } from "three";
import { InteractionStation } from "./InteractionStation";
import type { OptionalVectorRef, StationRef } from "./WorldEntry";
import {
  COMMAND_CENTER_BOUNDS,
  STATIONS,
  type StationId,
} from "./world-config";
import { clampPoint } from "./movement";

interface CommandCenterProps {
  movementTarget: OptionalVectorRef;
  pendingInteraction: StationRef;
  nearbyStation: StationId | null;
  onRequestMove: (x: number, z: number, stationId?: StationId | null) => void;
}

function CoreHologram() {
  const ring = useRef<Group>(null);

  useFrame((_, delta) => {
    if (ring.current) ring.current.rotation.y += delta * 0.35;
  });

  return (
    <group position={[0, 0, -0.4]}>
      <mesh position={[0, 0.16, 0]}>
        <cylinderGeometry args={[1.65, 1.9, 0.3, 32]} />
        <meshStandardMaterial color="#0b1b31" metalness={0.65} roughness={0.32} />
      </mesh>
      <group ref={ring} position={[0, 1.55, 0]}>
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
  pendingInteraction,
  nearbyStation,
  onRequestMove,
}: CommandCenterProps) {
  const handleFloorClick = (event: ThreeEvent<MouseEvent>) => {
    if (event.delta > 5) return;
    event.stopPropagation();
    const point = clampPoint({ x: event.point.x, z: event.point.z }, COMMAND_CENTER_BOUNDS);
    pendingInteraction.current = null;
    onRequestMove(point.x, point.z);
  };

  return (
    <>
      <fog attach="fog" args={["#050b15", 15, 34]} />
      <ambientLight intensity={0.72} />
      <directionalLight position={[5, 9, 5]} intensity={1.25} color="#cceaff" />
      <pointLight position={[0, 4, -1]} intensity={20} distance={12} color="#58d7ff" />
      <pointLight position={[5, 2.5, -3]} intensity={8} distance={7} color="#75f2c8" />

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow={false}
        onClick={handleFloorClick}
      >
        <planeGeometry args={[18, 14]} />
        <meshStandardMaterial color="#081426" metalness={0.22} roughness={0.7} />
      </mesh>

      <gridHelper args={[16, 16, "#173a58", "#0c2138"]} position={[0, 0.012, 0]} />

      <mesh position={[0, 1.5, -6.55]}>
        <boxGeometry args={[17.4, 3, 0.28]} />
        <meshStandardMaterial color="#081424" metalness={0.45} roughness={0.55} />
      </mesh>
      <mesh position={[-8.55, 0.75, 0]}>
        <boxGeometry args={[0.25, 1.5, 13]} />
        <meshStandardMaterial color="#0b1930" />
      </mesh>
      <mesh position={[8.55, 0.75, 0]}>
        <boxGeometry args={[0.25, 1.5, 13]} />
        <meshStandardMaterial color="#0b1930" />
      </mesh>

      <CoreHologram />

      {STATIONS.map((station) => (
        <InteractionStation
          key={station.id}
          station={station}
          nearby={nearbyStation === station.id}
          onSelect={() => {
            pendingInteraction.current = station.id;
            onRequestMove(
              station.interactionPoint.x,
              station.interactionPoint.z,
              station.id,
            );
          }}
        />
      ))}

      <MoveTargetMarker movementTarget={movementTarget} />

      <mesh position={[0, 0.38, 6.35]}>
        <boxGeometry args={[4.5, 0.75, 0.4]} />
        <meshStandardMaterial color="#102540" emissive="#0d2741" emissiveIntensity={0.45} />
      </mesh>
    </>
  );
}
