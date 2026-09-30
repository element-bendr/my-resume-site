import { useContext } from "react";
import type { RefObject } from "react";
import { Html } from "@react-three/drei";
import type { ThreeEvent } from "@react-three/fiber";
import { WorldLabelPortalContext } from "../app/world-label-portal";
import { BRIDGES, ZONES, type ZoneId } from "./world-topology";

interface WorldTopologyProps {
  currentZone: ZoneId;
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

export function WorldTopology({ currentZone, onRequestMove }: WorldTopologyProps) {
  const labelPortal = useContext(WorldLabelPortalContext);
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
              receiveShadow
              position={[geometry.centerX, -0.1, geometry.centerZ]}
              onClick={handleMove}
            >
              <boxGeometry args={[geometry.width, 0.18, geometry.depth]} />
              <meshStandardMaterial
                color={zone.id === "command-center" ? "#454b56" : "#343b47"}
                emissive={zone.accent}
                emissiveIntensity={0.025}
                metalness={0.12}
                roughness={0.72}
              />
            </mesh>
            <mesh position={[geometry.centerX, 0.005, zone.bounds.minZ + 0.12]}>
              <boxGeometry args={[Math.max(0.8, geometry.width - 0.45), 0.028, 0.055]} />
              <meshStandardMaterial
                color={zone.accent}
                emissive={zone.accent}
                emissiveIntensity={0.9}
                toneMapped={false}
              />
            </mesh>
            {zone.id !== "command-center" ? (
              <Html
                position={[geometry.centerX, 0.22, zone.bounds.minZ + 0.7]}
                center
                distanceFactor={14}
                transform
                sprite
                portal={(labelPortal as RefObject<HTMLElement> | null) ?? undefined}
              >
                <span
                  className="world-zone-label"
                  aria-hidden="true"
                  style={{ visibility: zone.id === currentZone ? "hidden" : "visible" }}
                >
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
            receiveShadow
            position={[geometry.centerX, -0.04, geometry.centerZ]}
            onClick={handleMove}
          >
            <boxGeometry args={[geometry.width, 0.12, geometry.depth]} />
            <meshStandardMaterial
              color="#2d3848"
              emissive="#3a8cc0"
              emissiveIntensity={0.08}
              metalness={0.34}
              roughness={0.48}
            />
          </mesh>
        );
      })}
    </group>
  );
}
