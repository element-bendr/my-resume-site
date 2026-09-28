import type { Point2, WorldBounds } from "./movement";

export type StationId = "newsharness" | "memory-os" | "ask-terminal";
export type StationKind = "project" | "ask";

export interface StationConfig {
  id: StationId;
  title: string;
  shortLabel: string;
  kind: StationKind;
  projectId?: string;
  position: readonly [number, number, number];
  interactionPoint: Point2;
  accent: string;
}

export const COMMAND_CENTER_BOUNDS: WorldBounds = {
  minX: -8,
  maxX: 8,
  minZ: -6,
  maxZ: 6,
};

export const PLAYER_SPAWN: Point2 = { x: 0, z: 3.5 };
export const WALK_SPEED = 3.5;
export const BRISK_WALK_SPEED = 5;
export const CLICK_WALK_SPEED = 4.2;
export const WALK_ACCELERATION_SECONDS = 1;
export const INTERACTION_RADIUS = 1.45;
export const TARGET_EPSILON = 0.08;

export const CAMERA = {
  position: [0, 6.4, 10.2] as const,
  targetHeight: 1,
  minDistance: 7,
  maxDistance: 11,
  minPolarAngle: 0.7,
  maxPolarAngle: 0.98,
  maxAzimuthAngle: Math.PI / 3,
};

export const STATIONS: readonly StationConfig[] = [
  {
    id: "newsharness",
    title: "Newsharness Signal Console",
    shortLabel: "Newsharness",
    kind: "project",
    projectId: "newsharness",
    position: [-4.35, 0, -2.7],
    interactionPoint: { x: -3.55, z: -1.45 },
    accent: "#58d7ff",
  },
  {
    id: "memory-os",
    title: "Memory OS Vault",
    shortLabel: "Memory OS",
    kind: "project",
    projectId: "memory-os",
    position: [-1.35, 0, -4.7],
    interactionPoint: { x: -1.35, z: -3.15 },
    accent: "#9a8cff",
  },
  {
    id: "ask-terminal",
    title: "Ask Terminal",
    shortLabel: "Ask",
    kind: "ask",
    position: [4.35, 0, -2.7],
    interactionPoint: { x: 3.55, z: -1.45 },
    accent: "#75f2c8",
  },
] as const;

export const STATION_BY_ID = Object.fromEntries(
  STATIONS.map((station) => [station.id, station]),
) as Record<StationId, StationConfig>;
