import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

export default function BuildLab(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[-9, 4, -17]} intensity={10} distance={10} color="#9a8cff" />

      <mesh position={[-9, 0.55, -20]}>
        <boxGeometry args={[7.5, 1.1, 0.45]} />
        <meshStandardMaterial color="#171a36" emissive="#2b235e" emissiveIntensity={0.45} />
      </mesh>

      {[-12.3, -10.1, -7.9, -5.7].map((x) => (
        <group key={x} position={[x, 0, -19.4]}>
          <mesh position={[0, 0.8, 0]}>
            <boxGeometry args={[1.25, 1.6, 0.7]} />
            <meshStandardMaterial color="#1a2540" metalness={0.48} roughness={0.42} />
          </mesh>
          <mesh position={[0, 1.15, 0.37]}>
            <boxGeometry args={[0.72, 0.42, 0.04]} />
            <meshStandardMaterial
              color="#b8abff"
              emissive="#7769d7"
              emissiveIntensity={0.9}
            />
          </mesh>
        </group>
      ))}

      <mesh position={[-9, 0.38, -14.9]}>
        <cylinderGeometry args={[1.4, 1.65, 0.7, 12]} />
        <meshStandardMaterial color="#151d37" metalness={0.55} roughness={0.36} />
      </mesh>
      <mesh position={[-9, 1.35, -14.9]}>
        <octahedronGeometry args={[0.62, 0]} />
        <meshStandardMaterial
          color="#d8d2ff"
          emissive="#9a8cff"
          emissiveIntensity={1.2}
          wireframe
        />
      </mesh>

      <DistrictStations zoneId="build-lab" {...props} />
    </group>
  );
}
