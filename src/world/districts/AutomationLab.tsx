import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

export default function AutomationLab(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[9, 4, -17]} intensity={11} distance={11} color="#75f2c8" />

      {[5.2, 7.7, 10.2, 12.7].map((x, index) => (
        <group key={x} position={[x, 0, -20]}>
          <mesh position={[0, 0.55, 0]}>
            <cylinderGeometry args={[0.36, 0.5, 1.1, 8]} />
            <meshStandardMaterial color="#0f3040" metalness={0.5} roughness={0.38} />
          </mesh>
          <mesh position={[0, 1.25, 0]}>
            <sphereGeometry args={[0.22 + index * 0.025, 12, 8]} />
            <meshStandardMaterial
              color="#d9fff3"
              emissive="#75f2c8"
              emissiveIntensity={1.15}
            />
          </mesh>
        </group>
      ))}

      <mesh position={[9.2, 0.12, -14.6]}>
        <boxGeometry args={[7.6, 0.18, 0.55]} />
        <meshStandardMaterial color="#143448" emissive="#1f6658" emissiveIntensity={0.42} />
      </mesh>

      {[6, 8.1, 10.2, 12.3].map((x) => (
        <mesh key={x} position={[x, 0.75, -14.6]}>
          <torusGeometry args={[0.38, 0.045, 8, 24]} />
          <meshStandardMaterial color="#75f2c8" emissive="#41a98a" emissiveIntensity={0.85} />
        </mesh>
      ))}

      <DistrictStations zoneId="automation-lab" {...props} />
    </group>
  );
}
