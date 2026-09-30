import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

export default function HobbyDistrict(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[17, 4, 0]} intensity={10} distance={11} color="#ff7fcf" />

      <mesh position={[17, 0.12, 0]}>
        <cylinderGeometry args={[2.2, 2.7, 0.22, 10]} />
        <meshStandardMaterial color="#2b1830" emissive="#5f2453" emissiveIntensity={0.38} />
      </mesh>

      <group position={[14.1, 0, 4.1]}>
        <mesh position={[0, 0.7, 0]}>
          <boxGeometry args={[1.1, 1.4, 0.7]} />
          <meshStandardMaterial color="#38223f" />
        </mesh>
        <mesh position={[0, 0.95, 0.37]}>
          <boxGeometry args={[0.72, 0.45, 0.04]} />
          <meshStandardMaterial color="#ffb3e7" emissive="#ff7fcf" emissiveIntensity={0.9} />
        </mesh>
      </group>

      <group position={[20.2, 0, 4.1]}>
        <mesh position={[0, 0.32, 0]}>
          <torusGeometry args={[0.48, 0.14, 10, 24]} />
          <meshStandardMaterial color="#342139" metalness={0.32} />
        </mesh>
        <mesh position={[0, 0.32, 0]}>
          <cylinderGeometry args={[0.14, 0.14, 0.85, 12]} />
          <meshStandardMaterial color="#e7a6d2" />
        </mesh>
      </group>

      <DistrictStations zoneId="hobby-district" {...props} />
    </group>
  );
}
