import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

function WorkBay({ x, labelGlow = "#9a8cff" }: { x: number; labelGlow?: string }) {
  return (
    <group position={[x, 0, -18.9]}>
      <mesh castShadow position={[0, 1.1, -0.45]}>
        <boxGeometry args={[1.75, 2.2, 0.18]} />
        <meshStandardMaterial color="#252a3b" metalness={0.34} roughness={0.52} />
      </mesh>
      <mesh position={[0, 1.25, -0.34]}>
        <boxGeometry args={[1.25, 0.68, 0.035]} />
        <meshStandardMaterial
          color="#cfc8ff"
          emissive={labelGlow}
          emissiveIntensity={0.82}
          toneMapped={false}
        />
      </mesh>
      <mesh castShadow position={[0, 0.42, 0.15]}>
        <boxGeometry args={[1.45, 0.16, 1.05]} />
        <meshStandardMaterial color="#34394a" metalness={0.36} roughness={0.48} />
      </mesh>
      <mesh position={[0, 0.68, 0.08]}>
        <boxGeometry args={[0.72, 0.46, 0.5]} />
        <meshStandardMaterial color="#16233a" metalness={0.28} roughness={0.48} />
      </mesh>
    </group>
  );
}

export default function BuildLab(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[-9, 4.5, -17]} intensity={6} distance={10} color="#a899ff" />
      <pointLight position={[-13, 2.5, -14]} intensity={2.4} distance={6} color="#ffbf7c" />

      <mesh castShadow position={[-9, 2.9, -20.2]}>
        <boxGeometry args={[10.2, 0.28, 0.34]} />
        <meshStandardMaterial color="#24293a" metalness={0.54} roughness={0.4} />
      </mesh>
      {[-13.4, -9, -4.6].map((x) => (
        <mesh key={x} castShadow position={[x, 1.5, -20.2]}>
          <boxGeometry args={[0.28, 3, 0.34]} />
          <meshStandardMaterial color="#30374a" metalness={0.46} roughness={0.44} />
        </mesh>
      ))}

      <WorkBay x={-12.4} />
      <WorkBay x={-9} labelGlow="#7f8cff" />
      <WorkBay x={-5.6} labelGlow="#c19cff" />

      <group position={[-9, 0, -14.7]}>
        <mesh receiveShadow position={[0, 0.3, 0]}>
          <cylinderGeometry args={[1.75, 1.95, 0.52, 16]} />
          <meshStandardMaterial color="#2e3448" metalness={0.45} roughness={0.44} />
        </mesh>
        <mesh position={[0, 1.45, 0]}>
          <boxGeometry args={[1.15, 1.15, 1.15]} />
          <meshStandardMaterial
            color="#d7d1ff"
            emissive="#8c7cff"
            emissiveIntensity={0.82}
            wireframe
            toneMapped={false}
          />
        </mesh>
        <mesh position={[0, 1.45, 0]} scale={0.72}>
          <boxGeometry args={[1.15, 1.15, 1.15]} />
          <meshBasicMaterial color="#907cff" transparent opacity={0.08} />
        </mesh>
      </group>

      <mesh position={[-14.55, 1.45, -16.2]}>
        <boxGeometry args={[0.08, 2.5, 5.8]} />
        <meshStandardMaterial
          color="#beaaff"
          emissive="#7d68ff"
          emissiveIntensity={0.75}
          toneMapped={false}
        />
      </mesh>

      <DistrictStations zoneId="build-lab" {...props} />
    </group>
  );
}
