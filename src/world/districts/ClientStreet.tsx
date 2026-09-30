import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

function Storefront({
  z,
  glow,
  width = 2.35,
}: {
  z: number;
  glow: string;
  width?: number;
}) {
  return (
    <group position={[-20.15, 0, z]}>
      <mesh castShadow position={[0, 1.35, 0]}>
        <boxGeometry args={[1.75, 2.7, width]} />
        <meshStandardMaterial color="#3b3337" roughness={0.6} />
      </mesh>
      <mesh position={[0.89, 1.25, 0]}>
        <boxGeometry args={[0.035, 1.45, width * 0.72]} />
        <meshPhysicalMaterial
          color="#ffd0a0"
          emissive={glow}
          emissiveIntensity={0.48}
          transparent
          opacity={0.55}
          roughness={0.16}
          metalness={0.05}
        />
      </mesh>
      <mesh position={[0.92, 2.35, 0]}>
        <boxGeometry args={[0.06, 0.38, width * 0.82]} />
        <meshStandardMaterial
          color="#ffe1b5"
          emissive={glow}
          emissiveIntensity={0.82}
          toneMapped={false}
        />
      </mesh>
      <mesh castShadow position={[1.35, 0.18, 0]}>
        <boxGeometry args={[0.82, 0.32, width * 0.85]} />
        <meshStandardMaterial color="#55504e" roughness={0.8} />
      </mesh>
    </group>
  );
}

export default function ClientStreet(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[-17.2, 4, 0]} intensity={5} distance={10} color="#ffc27e" />

      <Storefront z={-3.45} glow="#ff9b4b" />
      <Storefront z={-0.75} glow="#ffb56b" />
      <Storefront z={1.95} glow="#ff8b6b" />
      <Storefront z={4.05} glow="#ffc27e" width={1.55} />

      <mesh receiveShadow position={[-16.7, 0.015, 0]}>
        <boxGeometry args={[2.8, 0.06, 10.7]} />
        <meshStandardMaterial color="#414047" roughness={0.82} />
      </mesh>
      <mesh position={[-17.95, 0.075, 0]}>
        <boxGeometry args={[0.05, 0.025, 10.1]} />
        <meshStandardMaterial
          color="#ffd1a3"
          emissive="#ff9e55"
          emissiveIntensity={0.66}
          toneMapped={false}
        />
      </mesh>

      {[-4.3, 0, 4.3].map((z) => (
        <group key={z} position={[-15.45, 0, z]}>
          <mesh castShadow position={[0, 0.28, 0]}>
            <boxGeometry args={[0.75, 0.5, 0.75]} />
            <meshStandardMaterial color="#5b5550" roughness={0.9} />
          </mesh>
          <mesh position={[0, 0.75, 0]}>
            <sphereGeometry args={[0.42, 10, 8]} />
            <meshStandardMaterial color="#47734e" roughness={0.96} />
          </mesh>
        </group>
      ))}

      <DistrictStations zoneId="client-street" {...props} />
    </group>
  );
}
