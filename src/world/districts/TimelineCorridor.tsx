import { DistrictStations } from "./DistrictStations";
import type { DistrictProps } from "./types";

function MilestoneFrame({ x, height }: { x: number; height: number }) {
  return (
    <group position={[x, 0, 14.2]}>
      <mesh castShadow position={[-0.8, height / 2, 0]}>
        <boxGeometry args={[0.16, height, 0.2]} />
        <meshStandardMaterial color="#3a4152" metalness={0.38} roughness={0.48} />
      </mesh>
      <mesh castShadow position={[0.8, height / 2, 0]}>
        <boxGeometry args={[0.16, height, 0.2]} />
        <meshStandardMaterial color="#3a4152" metalness={0.38} roughness={0.48} />
      </mesh>
      <mesh position={[0, height, 0]}>
        <boxGeometry args={[1.8, 0.16, 0.2]} />
        <meshStandardMaterial color="#4a5060" metalness={0.38} roughness={0.46} />
      </mesh>
      <mesh position={[0, height * 0.62, 0.11]}>
        <boxGeometry args={[1.18, 0.72, 0.03]} />
        <meshStandardMaterial
          color="#fff1b4"
          emissive="#d5ae47"
          emissiveIntensity={0.55}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}

export default function TimelineCorridor(props: DistrictProps) {
  return (
    <group>
      <pointLight position={[0, 4.5, 18]} intensity={5.5} distance={12} color="#f5d477" />

      <mesh receiveShadow position={[0, 0.02, 17]}>
        <boxGeometry args={[12.4, 0.08, 2.35]} />
        <meshStandardMaterial color="#3d3e43" roughness={0.78} />
      </mesh>
      <mesh position={[0, 0.08, 15.95]}>
        <boxGeometry args={[11.8, 0.03, 0.04]} />
        <meshStandardMaterial
          color="#ffe28a"
          emissive="#e3b94b"
          emissiveIntensity={0.8}
          toneMapped={false}
        />
      </mesh>

      <MilestoneFrame x={-4.15} height={2.8} />
      <MilestoneFrame x={0} height={3.35} />
      <MilestoneFrame x={4.15} height={3.05} />

      {[-5.6, 5.6].map((x) => (
        <group key={x} position={[x, 0, 19.2]}>
          <mesh castShadow position={[0, 0.28, 0]}>
            <boxGeometry args={[0.72, 0.5, 1.5]} />
            <meshStandardMaterial color="#55534b" roughness={0.86} />
          </mesh>
          <mesh position={[0, 0.82, 0]}>
            <sphereGeometry args={[0.43, 10, 8]} />
            <meshStandardMaterial color="#506e4e" roughness={0.96} />
          </mesh>
        </group>
      ))}

      <DistrictStations zoneId="timeline" {...props} />
    </group>
  );
}
