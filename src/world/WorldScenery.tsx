import { BRIDGES, ZONES } from "./world-topology";

function dimensions(bounds: { minX: number; maxX: number; minZ: number; maxZ: number }) {
  return {
    width: bounds.maxX - bounds.minX,
    depth: bounds.maxZ - bounds.minZ,
    centerX: (bounds.minX + bounds.maxX) / 2,
    centerZ: (bounds.minZ + bounds.maxZ) / 2,
  };
}

function IslandUnderside({
  bounds,
  accent,
}: {
  bounds: { minX: number; maxX: number; minZ: number; maxZ: number };
  accent: string;
}) {
  const geometry = dimensions(bounds);
  const radius = Math.max(geometry.width, geometry.depth) * 0.46;

  return (
    <group position={[geometry.centerX, -0.38, geometry.centerZ]}>
      <mesh receiveShadow scale={[geometry.width * 0.55, 1.1, geometry.depth * 0.55]}>
        <dodecahedronGeometry args={[1, 0]} />
        <meshStandardMaterial color="#202735" roughness={0.92} metalness={0.04} />
      </mesh>
      <mesh position={[0, -1.35, 0]} scale={[radius * 0.8, 2.5, radius * 0.8]}>
        <coneGeometry args={[1, 2.8, 8]} />
        <meshStandardMaterial color="#151b28" roughness={1} />
      </mesh>
      <mesh position={[0, 0.15, 0]} scale={[geometry.width * 0.5, 0.12, geometry.depth * 0.5]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial
          color="#2c3547"
          emissive={accent}
          emissiveIntensity={0.035}
          roughness={0.7}
          metalness={0.18}
        />
      </mesh>
    </group>
  );
}

function BridgeArchitecture({
  bounds,
}: {
  bounds: { minX: number; maxX: number; minZ: number; maxZ: number };
}) {
  const geometry = dimensions(bounds);
  const alongX = geometry.width > geometry.depth;
  const railOffset = alongX ? geometry.depth / 2 - 0.12 : geometry.width / 2 - 0.12;
  const railLength = alongX ? geometry.width : geometry.depth;

  return (
    <group position={[geometry.centerX, 0, geometry.centerZ]}>
      <mesh position={[0, -0.22, 0]}>
        <boxGeometry args={[geometry.width, 0.3, geometry.depth]} />
        <meshStandardMaterial color="#222d3d" metalness={0.35} roughness={0.58} />
      </mesh>

      {[-1, 1].map((side) => (
        <group
          key={side}
          position={
            alongX
              ? [0, 0.34, side * railOffset]
              : [side * railOffset, 0.34, 0]
          }
        >
          <mesh>
            <boxGeometry
              args={alongX ? [railLength, 0.055, 0.055] : [0.055, 0.055, railLength]}
            />
            <meshStandardMaterial
              color="#9fcfff"
              emissive="#4ca8ff"
              emissiveIntensity={0.85}
              metalness={0.55}
              roughness={0.28}
            />
          </mesh>
          <mesh position={[0, -0.3, 0]}>
            <boxGeometry
              args={alongX ? [railLength, 0.03, 0.03] : [0.03, 0.03, railLength]}
            />
            <meshBasicMaterial color="#4ca8ff" transparent opacity={0.55} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function Waterfall({ x, z, rotation = 0 }: { x: number; z: number; rotation?: number }) {
  return (
    <group position={[x, -2.4, z]} rotation={[0, rotation, 0]}>
      <mesh>
        <planeGeometry args={[1.45, 5.4, 1, 1]} />
        <meshBasicMaterial color="#65cfff" transparent opacity={0.2} depthWrite={false} />
      </mesh>
      <mesh position={[0, 0, -0.015]}>
        <planeGeometry args={[0.52, 5.1, 1, 1]} />
        <meshBasicMaterial color="#d4f6ff" transparent opacity={0.27} depthWrite={false} />
      </mesh>
    </group>
  );
}

export function WorldScenery() {
  return (
    <group>
      {ZONES.map((zone) => (
        <IslandUnderside key={zone.id} bounds={zone.bounds} accent={zone.accent} />
      ))}

      {BRIDGES.map((bridge) => (
        <BridgeArchitecture key={bridge.id} bounds={bridge.bounds} />
      ))}

      <Waterfall x={-6.7} z={5.75} />
      <Waterfall x={6.7} z={5.75} rotation={Math.PI} />
      <Waterfall x={-21.8} z={1.8} rotation={Math.PI / 2} />
      <Waterfall x={21.8} z={-1.8} rotation={-Math.PI / 2} />
    </group>
  );
}
