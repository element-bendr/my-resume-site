import type { ThreeEvent } from "@react-three/fiber";
import { useFrame } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import { Group } from "three";
import type { StationConfig } from "./world-config";

interface InteractionStationProps {
  station: StationConfig;
  nearby: boolean;
  onSelect: () => void;
}

export function InteractionStation({ station, nearby, onSelect }: InteractionStationProps) {
  const [hovered, setHovered] = useState(false);
  const animated = useRef<Group>(null);
  const active = hovered || nearby;

  useEffect(() => {
    return () => {
      if (hovered) document.body.style.cursor = "";
    };
  }, [hovered]);

  useFrame((state, delta) => {
    if (!animated.current) return;
    animated.current.rotation.y += delta * 0.25;
    animated.current.position.y = 1.52 + Math.sin(state.clock.elapsedTime * 1.8) * 0.035;
  });

  const select = (event: ThreeEvent<MouseEvent>) => {
    if (event.delta > 5) return;
    event.stopPropagation();
    onSelect();
  };

  return (
    <group position={[station.position[0], station.position[1], station.position[2]]}>
      <mesh position={[0, 0.42, 0]} onClick={select}>
        <cylinderGeometry args={[0.72, 0.88, 0.84, 8]} />
        <meshStandardMaterial color="#0d1d32" metalness={0.65} roughness={0.4} />
      </mesh>

      <mesh
        position={[0, 1.08, 0]}
        rotation={[-0.16, 0, 0]}
        onClick={select}
        onPointerOver={(event) => {
          event.stopPropagation();
          setHovered(true);
          document.body.style.cursor = "pointer";
        }}
        onPointerOut={() => {
          setHovered(false);
          document.body.style.cursor = "";
        }}
      >
        <boxGeometry args={[1.15, 0.7, 0.13]} />
        <meshStandardMaterial
          color={active ? station.accent : "#172a43"}
          emissive={active ? station.accent : "#07101e"}
          emissiveIntensity={active ? 1.2 : 0.25}
          metalness={0.28}
          roughness={0.38}
        />
      </mesh>

      <group ref={animated} position={[0, 1.52, 0]}>
        <mesh rotation={[Math.PI / 2, 0, 0]} onClick={select}>
          <torusGeometry args={[0.38, 0.025, 8, 28]} />
          <meshBasicMaterial color={station.accent} transparent opacity={active ? 0.95 : 0.5} />
        </mesh>
        {station.kind === "ask" ? (
          <mesh onClick={select}>
            <octahedronGeometry args={[0.2, 0]} />
            <meshStandardMaterial color={station.accent} emissive={station.accent} emissiveIntensity={1} />
          </mesh>
        ) : (
          <mesh onClick={select}>
            <boxGeometry args={[0.28, 0.28, 0.28]} />
            <meshStandardMaterial color={station.accent} emissive={station.accent} emissiveIntensity={0.8} />
          </mesh>
        )}
      </group>

      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.018, 0]}>
        <ringGeometry args={[0.92, 1.02, 32]} />
        <meshBasicMaterial color={station.accent} transparent opacity={nearby ? 0.8 : 0.2} />
      </mesh>
    </group>
  );
}
