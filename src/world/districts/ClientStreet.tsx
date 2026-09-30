import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

export default function ClientStreet(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[-17, 4, 0]} intensity={9} distance={10} color="#ffb86b" />

      <mesh position={[-21.3, 1.45, 0]}>
        <boxGeometry args={[0.5, 2.9, 10.3]} />
        <meshStandardMaterial color="#2b1c20" metalness={0.18} roughness={0.68} />
      </mesh>

      {[-3.5, -0.8, 1.9, 4.1].map((z, index) => (
        <group key={z} position={[-20.7, 0, z]}>
          <mesh position={[0.7, 1.05, 0]}>
            <boxGeometry args={[1.45, 2.1, 1.9]} />
            <meshStandardMaterial
              color={index % 2 === 0 ? "#2d2735" : "#26313a"}
              roughness={0.62}
            />
          </mesh>
          <mesh position={[1.43, 1.05, 0]}>
            <boxGeometry args={[0.04, 0.78, 1.05]} />
            <meshStandardMaterial
              color="#ffd3a5"
              emissive="#b46b32"
              emissiveIntensity={0.72}
            />
          </mesh>
        </group>
      ))}

      <mesh position={[-16.8, 0.04, 0]}>
        <boxGeometry args={[2.2, 0.08, 10.5]} />
        <meshStandardMaterial color="#211a1c" roughness={0.82} />
      </mesh>

      <DistrictStations zoneId="client-street" {...props} />
    </group>
  );
}
