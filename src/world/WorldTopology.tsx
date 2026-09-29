import { Html } from "@react-three/drei";
import type { ThreeEvent } from "@react-three/fiber";
import { BRIDGES, ZONES } from "./world-topology";

interface WorldTopologyProps {
  onRequestMove: (x: number, z: number) => void;
}

function boundsGeometry(bounds: { minX: number; maxX: number; minZ: number; maxZ: number }) {
  return {
    width: bounds.maxX - bounds.minX,
    depth: bounds.maxZ - bounds.minZ,
    centerX: (bounds.minX + bounds.maxX) / 2,
    centerZ: (bounds.minZ + bounds.maxZ) / 2,
  };
}

export function WorldTopology({ onRequestMove }: WorldTopologyProps) {
  const handleMove = (event: ThreeEvent<MouseEvent>) => {
    if (event.delta > 5) return;
    event.stopPropagation();
    onRequestMove(event.point.x, event.point.z);
  };

  return (
    <group>
      {ZONES.map((zone) => {
        const geometry = boundsGeometry(zone.bounds);
        return (
          <group key={zone.id}>
            <mesh
              position={[geometry.centerX, -0.13, geometry.centerZ]}
              onClick={handleMove}
            >
              <boxGeometry args={[geometry.width, 0.24, geometry.depth]} />
              <meshStandardMaterial
                color="#071426"
                emissive={zone.accent}
                emissiveIntensity={0.035}
                metalness={0.16}
                roughness={0.78}
              />
            </mesh>
            {zone.id !== "command-center" ? (
              <Html
                position={[geometry.centerX, 0.22, zone.bounds.maxZ - 0.7]}
                center
                distanceFactor={14}
                transform
                sprite
              >
                <span className="world-zone-label" aria-hidden="true">
                  {zone.label}
                </span>
              </Html>
            ) : null}
          </group>
        );
      })}

      {BRIDGES.map((bridge) => {
        const geometry = boundsGeometry(bridge.bounds);
        return (
          <mesh
            key={bridge.id}
            position={[geometry.centerX, -0.08, geometry.centerZ]}
            onClick={handleMove}
          >
            <boxGeometry args={[geometry.width, 0.14, geometry.depth]} />
            <meshStandardMaterial
              color="#0a2137"
              emissive="#153d5c"
              emissiveIntensity={0.28}
              metalness={0.35}
              roughness={0.52}
            />
          </mesh>
        );
      })}
    </group>
  );
}
