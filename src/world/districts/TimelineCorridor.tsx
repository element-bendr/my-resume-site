import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

export default function TimelineCorridor(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[0, 4, 18]} intensity={10} distance={11} color="#f4d06f" />

      <mesh position={[0, 0.09, 18.3]}>
        <boxGeometry args={[11, 0.16, 0.32]} />
        <meshStandardMaterial color="#4a3a17" emissive="#8c6d25" emissiveIntensity={0.45} />
      </mesh>

      {[-4.1, 0, 4.1].map((x, index) => (
        <group key={x} position={[x, 0, 20.4]}>
          <mesh position={[0, 1.25, 0]}>
            <boxGeometry args={[0.26, 2.5, 0.26]} />
            <meshStandardMaterial color="#5c4920" metalness={0.35} roughness={0.48} />
          </mesh>
          <mesh position={[0, 2.55, 0]}>
            <sphereGeometry args={[0.22 + index * 0.035, 12, 8]} />
            <meshStandardMaterial
              color="#fff0ac"
              emissive="#f4d06f"
              emissiveIntensity={1.15}
            />
          </mesh>
        </group>
      ))}

      <DistrictStations zoneId="timeline" {...props} />
    </group>
  );
}
