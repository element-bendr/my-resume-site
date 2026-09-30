import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

function DataTower({ x, z, height }: { x: number; z: number; height: number }) {
  return (
    <group position={[x, 0, z]}>
      <mesh castShadow position={[0, height / 2, 0]}>
        <cylinderGeometry args={[0.48, 0.62, height, 10]} />
        <meshStandardMaterial color="#183640" metalness={0.5} roughness={0.4} />
      </mesh>
      {[0.45, 0.95, 1.45].filter((y) => y < height).map((y) => (
        <mesh key={y} position={[0, y, 0]}>
          <torusGeometry args={[0.54, 0.025, 8, 28]} />
          <meshStandardMaterial
            color="#8affda"
            emissive="#45e1b0"
            emissiveIntensity={1}
            toneMapped={false}
          />
        </mesh>
      ))}
    </group>
  );
}

export default function AutomationLab(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[9, 4.5, -17]} intensity={6} distance={11} color="#72f2c8" />
      <pointLight position={[13, 2.8, -15]} intensity={2.5} distance={7} color="#67dfff" />

      <mesh castShadow position={[9, 2.4, -20.2]}>
        <boxGeometry args={[10.2, 0.22, 0.3]} />
        <meshStandardMaterial color="#1d343c" metalness={0.52} roughness={0.42} />
      </mesh>

      <DataTower x={5.4} z={-19.1} height={2.3} />
      <DataTower x={7.9} z={-19.6} height={3} />
      <DataTower x={10.5} z={-19.3} height={2.55} />
      <DataTower x={13} z={-19.7} height={3.2} />

      <group position={[9.1, 0, -14.7]}>
        <mesh receiveShadow position={[0, 0.28, 0]}>
          <cylinderGeometry args={[1.65, 1.95, 0.48, 18]} />
          <meshStandardMaterial color="#253941" metalness={0.48} roughness={0.4} />
        </mesh>
        <mesh position={[0, 1.25, 0]}>
          <cylinderGeometry args={[0.68, 0.82, 1.8, 12]} />
          <meshPhysicalMaterial
            color="#5affcb"
            emissive="#32d6a1"
            emissiveIntensity={0.6}
            transparent
            opacity={0.28}
            transmission={0.18}
            roughness={0.18}
            metalness={0.1}
            toneMapped={false}
          />
        </mesh>
        <mesh position={[0, 1.25, 0]}>
          <torusGeometry args={[1.02, 0.035, 8, 40]} />
          <meshStandardMaterial
            color="#7dffe0"
            emissive="#41dfb2"
            emissiveIntensity={1.2}
            toneMapped={false}
          />
        </mesh>
      </group>

      <mesh position={[4.15, 1.2, -16.4]}>
        <boxGeometry args={[0.06, 2.2, 6.8]} />
        <meshStandardMaterial
          color="#6fffd5"
          emissive="#3bcda3"
          emissiveIntensity={0.66}
          toneMapped={false}
        />
      </mesh>

      <DistrictStations zoneId="automation-lab" {...props} />
    </group>
  );
}
