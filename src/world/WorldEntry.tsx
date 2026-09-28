import { Canvas } from "@react-three/fiber";
import { useCallback, useEffect, useRef, useState } from "react";
import { Vector3 } from "three";
import { CameraRig } from "./CameraRig";
import { CommandCenter } from "./CommandCenter";
import { InteractionOverlay } from "./InteractionOverlay";
import { PlayerController } from "./PlayerController";
import { WorldCanvasBoundary } from "./WorldCanvasBoundary";
import { WebGLFallback } from "./WebGLFallback";
import { WorldHud } from "./WorldHud";
import { detectWebGLSupport } from "./webgl";
import {
  CAMERA,
  COMMAND_CENTER_BOUNDS,
  PLAYER_SPAWN,
  STATION_BY_ID,
  type StationId,
} from "./world-config";
import { clampPoint } from "./movement";
import "./world.css";

export interface VectorRef {
  current: Vector3;
}

export interface OptionalVectorRef {
  current: Vector3 | null;
}

export interface StationRef {
  current: StationId | null;
}

function useReducedMotion() {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReducedMotion(query.matches);
    update();
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);

  return reducedMotion;
}

export default function WorldEntry() {
  const playerPosition = useRef(new Vector3(PLAYER_SPAWN.x, 0, PLAYER_SPAWN.z));
  const movementTarget = useRef<Vector3 | null>(null);
  const pendingInteraction = useRef<StationId | null>(null);
  const [nearbyStation, setNearbyStation] = useState<StationId | null>(null);
  const [activeStation, setActiveStation] = useState<StationId | null>(null);
  const [mapOpen, setMapOpen] = useState(false);
  const reducedMotion = useReducedMotion();
  const [webglAvailable] = useState(() => detectWebGLSupport());

  const requestMove = useCallback((x: number, z: number, stationId: StationId | null = null) => {
    const point = clampPoint({ x, z }, COMMAND_CENTER_BOUNDS);
    movementTarget.current = new Vector3(point.x, 0, point.z);
    pendingInteraction.current = stationId;
  }, []);

  const closeOverlay = useCallback(() => setActiveStation(null), []);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      if (activeStation) closeOverlay();
      else if (mapOpen) setMapOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [activeStation, closeOverlay, mapOpen]);

  return (
    <div className="world-shell">
      <div className="world-canvas" aria-label="Interactive Command Center portfolio world">
        {webglAvailable ? (
          <WorldCanvasBoundary fallback={<WebGLFallback />}>
            <Canvas
              camera={{
                position: [CAMERA.position[0], CAMERA.position[1], CAMERA.position[2]],
                fov: 50,
                near: 0.1,
                far: 60,
              }}
              dpr={[1, 1.5]}
              gl={{ antialias: true, powerPreference: "high-performance" }}
              fallback={<WebGLFallback />}
            >
              <CommandCenter
                movementTarget={movementTarget}
                pendingInteraction={pendingInteraction}
                nearbyStation={nearbyStation}
                onRequestMove={requestMove}
              />
              <PlayerController
                playerPosition={playerPosition}
                movementTarget={movementTarget}
                pendingInteraction={pendingInteraction}
                controlsEnabled={!activeStation && !mapOpen}
                onInteract={setActiveStation}
                onNearestChange={setNearbyStation}
              />
              <CameraRig playerPosition={playerPosition} reducedMotion={reducedMotion} />
            </Canvas>
          </WorldCanvasBoundary>
        ) : (
          <WebGLFallback />
        )}
      </div>

      <WorldHud
        nearbyStation={nearbyStation ? STATION_BY_ID[nearbyStation] : null}
        mapOpen={mapOpen}
        onToggleMap={() => setMapOpen((open) => !open)}
        onCloseMap={() => setMapOpen(false)}
      />

      {activeStation ? (
        <InteractionOverlay station={STATION_BY_ID[activeStation]} onClose={closeOverlay} />
      ) : null}
    </div>
  );
}
