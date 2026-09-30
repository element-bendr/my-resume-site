import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

function BlossomTree({ x, z, scale = 1 }: { x: number; z: number; scale?: number }) {
  return (
    <group position={[x, 0, z]} scale={scale}>
      <mesh castShadow position={[0, 0.8, 0]}>
        <cylinderGeometry args={[0.12, 0.18, 1.6, 7]} />
        <meshStandardMaterial color="#4a2e35" roughness={0.95} />
      </mesh>
      {[
        [0, 1.65, 0],
        [0.42, 1.55, 0.08],
        [-0.42, 1.52, -0.04],
        [0.14, 1.85, -0.26],
      ].map(([px, py, pz], index) => (
        <mesh key={index} position={[px, py, pz]}>
          <sphereGeometry args={[0.48, 9, 7]} />
          <meshStandardMaterial color={index % 2 ? "#ff9bd6" : "#ff7fcf"} roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

export default function HobbyDistrict(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[17, 4.5, 0]} intensity={5.5} distance={11} color="#ff83d1" />

      <mesh receiveShadow position={[17, 0.04, 0]}>
        <cylinderGeometry args={[3, 3.35, 0.12, 18]} />
        <meshStandardMaterial color="#47404b" roughness={0.8} />
      </mesh>
      <mesh position={[17, 0.12, 0]}>
        <torusGeometry args={[2.55, 0.045, 8, 56]} />
        <meshStandardMaterial
          color="#ffb2e4"
          emissive="#ff68c2"
          emissiveIntensity={0.82}
          toneMapped={false}
        />
      </mesh>

      <group position={[14.1, 0, 3.8]}>
        <mesh castShadow position={[0, 0.85, 0]}>
          <boxGeometry args={[1.45, 1.7, 0.85]} />
          <meshStandardMaterial color="#34273b" metalness={0.12} roughness={0.58} />
        </mesh>
        <mesh position={[0, 1.02, 0.44]}>
          <boxGeometry args={[0.95, 0.62, 0.035]} />
          <meshStandardMaterial
            color="#ffc0ea"
            emissive="#ff6fc7"
            emissiveIntensity={0.8}
            toneMapped={false}
          />
        </mesh>
      </group>

      <group position={[20.15, 0, 3.8]}>
        <mesh castShadow position={[0, 0.38, 0]}>
          <torusGeometry args={[0.58, 0.16, 10, 28]} />
          <meshStandardMaterial color="#2b2531" metalness={0.4} roughness={0.5} />
        </mesh>
        <mesh position={[0, 0.38, 0]}>
          <cylinderGeometry args={[0.14, 0.14, 1.05, 12]} />
          <meshStandardMaterial color="#f6b8dd" roughness={0.5} />
        </mesh>
      </group>

      <BlossomTree x={14.2} z={-4.15} />
      <BlossomTree x={20} z={-4.1} scale={1.1} />
      <BlossomTree x={21} z={1.4} scale={0.82} />

      <mesh position={[17, 0.07, -3.85]}>
        <boxGeometry args={[4.7, 0.06, 0.04]} />
        <meshStandardMaterial
          color="#ffafe1"
          emissive="#ff65c2"
          emissiveIntensity={0.72}
          toneMapped={false}
        />
      </mesh>

      <DistrictStations zoneId="hobby-district" {...props} />
    </group>
  );
}
