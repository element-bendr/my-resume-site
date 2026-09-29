import { Canvas } from "@react-three/fiber";
import { useCallback, useEffect, useRef, useState } from "react";
import { Vector3 } from "three";
import { CameraRig } from "./CameraRig";
import { CommandCenter } from "./CommandCenter";
import { InteractionOverlay } from "./InteractionOverlay";
import { PlayerController } from "./PlayerController";
import { WorldCanvasBoundary } from "./WorldCanvasBoundary";
import { WorldDistricts } from "./WorldDistricts";
import { WorldHud } from "./WorldHud";
import { WorldTopology } from "./WorldTopology";
import { WebGLFallback } from "./WebGLFallback";
import { detectWebGLSupport } from "./webgl";
import {
  CAMERA,
  PLAYER_SPAWN,
  STATION_BY_ID,
  type StationConfig,
  type StationId,
} from "./world-config";
import {
  ZONE_BY_ID,
  parseZoneId,
  type ZoneId,
} from "./world-topology";
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
  const initialZone = parseZoneId(
    typeof window === "undefined"
      ? null
      : new URLSearchParams(window.location.search).get("zone"),
  ) ?? "command-center";
  const initialPoint = ZONE_BY_ID[initialZone].fastTravelPoint;
  const playerPosition = useRef(new Vector3(initialPoint.x, 0, initialPoint.z));
  const movementTarget = useRef<Vector3 | null>(null);
  const pendingInteraction = useRef<StationId | null>(null);
  const [nearbyStation, setNearbyStation] = useState<StationId | null>(null);
  const [activeStation, setActiveStation] = useState<StationId | null>(null);
  const [currentZone, setCurrentZone] = useState<ZoneId>(initialZone);
  const [loadedZones, setLoadedZones] = useState<Set<ZoneId>>(
    () => new Set<ZoneId>(["command-center", initialZone]),
  );
  const [mapOpen, setMapOpen] = useState(false);
  const reducedMotion = useReducedMotion();
  const [webglAvailable] = useState(() => detectWebGLSupport());

  const loadZone = useCallback((zone: ZoneId) => {
    setLoadedZones((current) => {
      if (current.has(zone)) return current;
      const next = new Set(current);
      next.add(zone);
      return next;
    });
  }, []);

  const requestMove = useCallback((x: number, z: number, stationId: StationId | null = null) => {
    movementTarget.current = new Vector3(x, 0, z);
    pendingInteraction.current = stationId;
  }, []);

  const selectStation = useCallback(
    (station: StationConfig) => {
      loadZone(station.zoneId);
      requestMove(station.interactionPoint.x, station.interactionPoint.z, station.id);
    },
    [loadZone, requestMove],
  );

  const handleZoneChange = useCallback(
    (zone: ZoneId) => {
      setCurrentZone(zone);
      loadZone(zone);
    },
    [loadZone],
  );

  const fastTravel = useCallback(
    (zone: ZoneId) => {
      const target = ZONE_BY_ID[zone].fastTravelPoint;
      loadZone(zone);
      movementTarget.current = null;
      pendingInteraction.current = null;
      playerPosition.current.set(target.x, 0, target.z);
      setNearbyStation(null);
      setActiveStation(null);
      setCurrentZone(zone);
      if (typeof window !== "undefined") {
        const url = new URL(window.location.href);
        if (zone === "command-center") url.searchParams.delete("zone");
        else url.searchParams.set("zone", zone);
        window.history.replaceState(null, "", url);
      }
      setMapOpen(false);
    },
    [loadZone],
  );

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
      <div className="world-canvas" aria-label="Interactive Portfolio World">
        {webglAvailable ? (
          <WorldCanvasBoundary fallback={<WebGLFallback />}>
            <Canvas
              camera={{
                position: [CAMERA.position[0], CAMERA.position[1], CAMERA.position[2]],
                fov: 52,
                near: 0.1,
                far: 90,
              }}
              dpr={[1, 1.5]}
              gl={{ antialias: true, powerPreference: "high-performance" }}
              fallback={<WebGLFallback />}
            >
              <WorldTopology onRequestMove={(x, z) => requestMove(x, z)} />
              <CommandCenter
                movementTarget={movementTarget}
                nearbyStation={nearbyStation}
                onSelectStation={selectStation}
              />
              <WorldDistricts
                loadedZones={loadedZones}
                nearbyStationId={nearbyStation}
                onSelectStation={selectStation}
              />
              <PlayerController
                playerPosition={playerPosition}
                movementTarget={movementTarget}
                pendingInteraction={pendingInteraction}
                controlsEnabled={!activeStation && !mapOpen}
                onInteract={setActiveStation}
                onNearestChange={setNearbyStation}
                onZoneChange={handleZoneChange}
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
        currentZone={currentZone}
        mapOpen={mapOpen}
        onToggleMap={() => setMapOpen((open) => !open)}
        onCloseMap={() => setMapOpen(false)}
        onFastTravel={fastTravel}
      />

      {activeStation ? (
        <InteractionOverlay station={STATION_BY_ID[activeStation]} onClose={closeOverlay} />
      ) : null}
    </div>
  );
}
