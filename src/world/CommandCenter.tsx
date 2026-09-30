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
  reducedMotion: boolean;
}

function PlazaPylon({ x, z, rotation = 0 }: { x: number; z: number; rotation?: number }) {
  return (
    <group position={[x, 0, z]} rotation={[0, rotation, 0]}>
      <mesh castShadow position={[0, 1.8, 0]}>
        <boxGeometry args={[0.72, 3.6, 0.72]} />
        <meshStandardMaterial color="#273247" metalness={0.42} roughness={0.42} />
      </mesh>
      <mesh position={[0, 2.15, 0.365]}>
        <boxGeometry args={[0.38, 1.55, 0.025]} />
        <meshStandardMaterial
          color="#9fe9ff"
          emissive="#4cc8ff"
          emissiveIntensity={1.15}
          toneMapped={false}
        />
      </mesh>
      <mesh castShadow position={[0, 3.9, 0]}>
        <coneGeometry args={[0.45, 1.2, 5]} />
        <meshStandardMaterial color="#303d55" metalness={0.48} roughness={0.36} />
      </mesh>
    </group>
  );
}

function CoreHologram({ reducedMotion }: { reducedMotion: boolean }) {
  const ring = useRef<Group>(null);
  const globe = useRef<Group>(null);

  useFrame((_, delta) => {
    if (reducedMotion) return;
    if (ring.current) ring.current.rotation.y += delta * 0.22;
    if (globe.current) globe.current.rotation.y -= delta * 0.1;
  });

  return (
    <group position={[0, 0, 0.65]}>
      <mesh receiveShadow position={[0, 0.08, 0]}>
        <cylinderGeometry args={[2.2, 2.55, 0.16, 48]} />
        <meshStandardMaterial color="#2b3446" metalness={0.42} roughness={0.46} />
      </mesh>
      <mesh position={[0, 0.2, 0]}>
        <torusGeometry args={[1.75, 0.045, 10, 64]} />
        <meshStandardMaterial
          color="#9cecff"
          emissive="#4ccfff"
          emissiveIntensity={1.4}
          toneMapped={false}
        />
      </mesh>

      <group ref={ring} position={[0, 2.45, 0]}>
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[1.42, 0.035, 12, 64]} />
          <meshStandardMaterial
            color="#8ce8ff"
            emissive="#3bbcff"
            emissiveIntensity={1.5}
            toneMapped={false}
          />
        </mesh>
        <mesh rotation={[0.42, 0, 0.25]}>
          <torusGeometry args={[1.15, 0.025, 10, 56]} />
          <meshStandardMaterial
            color="#b9aaff"
            emissive="#816cff"
            emissiveIntensity={1.25}
            toneMapped={false}
          />
        </mesh>
        <group ref={globe}>
          <mesh>
            <sphereGeometry args={[0.9, 24, 18]} />
            <meshStandardMaterial
              color="#c8f4ff"
              emissive="#4dcfff"
              emissiveIntensity={0.95}
              wireframe
              transparent
              opacity={0.9}
              toneMapped={false}
            />
          </mesh>
          <mesh scale={0.84}>
            <sphereGeometry args={[0.9, 18, 12]} />
            <meshBasicMaterial color="#5dcfff" transparent opacity={0.08} />
          </mesh>
        </group>
      </group>

      <pointLight position={[0, 2.4, 0]} intensity={6} distance={8} color="#5ad8ff" />
    </group>
  );
}

function PlazaArchitecture() {
  return (
    <group>
      <mesh receiveShadow position={[0, -0.02, 0]}>
        <cylinderGeometry args={[5.2, 5.55, 0.18, 48]} />
        <meshStandardMaterial color="#313a49" metalness={0.28} roughness={0.62} />
      </mesh>
      <mesh receiveShadow position={[0, 0.04, 0]}>
        <cylinderGeometry args={[3.8, 4.15, 0.18, 48]} />
        <meshStandardMaterial color="#e6e0cf" metalness={0.08} roughness={0.72} />
      </mesh>
      <mesh position={[0, 0.16, 0]}>
        <torusGeometry args={[4.45, 0.045, 8, 80]} />
        <meshStandardMaterial
          color="#b9eaff"
          emissive="#53c9ff"
          emissiveIntensity={0.75}
          toneMapped={false}
        />
      </mesh>

      <PlazaPylon x={-4.5} z={-3.1} rotation={0.16} />
      <PlazaPylon x={4.5} z={-3.1} rotation={-0.16} />
      <PlazaPylon x={-4.5} z={3.1} rotation={Math.PI - 0.16} />
      <PlazaPylon x={4.5} z={3.1} rotation={Math.PI + 0.16} />

      {[-1, 1].flatMap((x) =>
        [-1, 1].map((z) => (
          <group key={`${x}-${z}`} position={[x * 3.15, 0, z * 2.35]}>
            <mesh castShadow position={[0, 0.38, 0]}>
              <boxGeometry args={[1.25, 0.72, 0.9]} />
              <meshStandardMaterial color="#4b5564" roughness={0.7} />
            </mesh>
            <mesh position={[0, 0.77, 0]}>
              <boxGeometry args={[1.05, 0.12, 0.7]} />
              <meshStandardMaterial color="#273448" metalness={0.2} roughness={0.55} />
            </mesh>
          </group>
        )),
      )}
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
  reducedMotion,
}: CommandCenterProps) {
  const commandStations = stationsForZone("command-center");

  return (
    <>
      <PlazaArchitecture />
      <CoreHologram reducedMotion={reducedMotion} />

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
