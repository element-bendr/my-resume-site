import type { Point2, WorldBounds } from "./movement";
import { constrainPointToAreas, pointInBounds } from "./movement";

export type ZoneId =
  | "command-center"
  | "build-lab"
  | "automation-lab"
  | "client-street"
  | "timeline"
  | "hobby-district";

export interface ZoneConfig {
  id: ZoneId;
  label: string;
  shortLabel: string;
  accent: string;
  bounds: WorldBounds;
  fastTravelPoint: Point2;
}

export interface WalkableArea {
  id: string;
  kind: "zone" | "bridge";
  bounds: WorldBounds;
  zoneId?: ZoneId;
  connects?: readonly [ZoneId, ZoneId];
}

export const COMMAND_CENTER_BOUNDS: WorldBounds = {
  minX: -8,
  maxX: 8,
  minZ: -6,
  maxZ: 6,
};

export const ZONES: readonly ZoneConfig[] = [
  {
    id: "command-center",
    label: "Command Center",
    shortLabel: "Command",
    accent: "#63d8ff",
    bounds: COMMAND_CENTER_BOUNDS,
    fastTravelPoint: { x: 0, z: 3.5 },
  },
  {
    id: "client-street",
    label: "Client Street",
    shortLabel: "Clients",
    accent: "#ffb86b",
    bounds: { minX: -22, maxX: -12, minZ: -6, maxZ: 6 },
    fastTravelPoint: { x: -17, z: 2.8 },
  },
  {
    id: "hobby-district",
    label: "Hobby District",
    shortLabel: "Hobbies",
    accent: "#ff7fcf",
    bounds: { minX: 12, maxX: 22, minZ: -6, maxZ: 6 },
    fastTravelPoint: { x: 17, z: 2.8 },
  },
  {
    id: "timeline",
    label: "Timeline Corridor",
    shortLabel: "Timeline",
    accent: "#f4d06f",
    bounds: { minX: -7, maxX: 7, minZ: 12, maxZ: 22 },
    fastTravelPoint: { x: 0, z: 14.2 },
  },
  {
    id: "build-lab",
    label: "Build Lab",
    shortLabel: "Build",
    accent: "#9a8cff",
    bounds: { minX: -15, maxX: -3, minZ: -21, maxZ: -11 },
    fastTravelPoint: { x: -9, z: -13.2 },
  },
  {
    id: "automation-lab",
    label: "Automation Lab",
    shortLabel: "Automation",
    accent: "#75f2c8",
    bounds: { minX: 3, maxX: 15, minZ: -21, maxZ: -11 },
    fastTravelPoint: { x: 9, z: -13.2 },
  },
] as const;

export const ZONE_BY_ID = Object.fromEntries(
  ZONES.map((zone) => [zone.id, zone]),
) as Record<ZoneId, ZoneConfig>;

export const BRIDGES: readonly WalkableArea[] = [
  {
    id: "bridge-client",
    kind: "bridge",
    bounds: { minX: -12.5, maxX: -7.5, minZ: -1.5, maxZ: 1.5 },
    connects: ["command-center", "client-street"],
  },
  {
    id: "bridge-hobby",
    kind: "bridge",
    bounds: { minX: 7.5, maxX: 12.5, minZ: -1.5, maxZ: 1.5 },
    connects: ["command-center", "hobby-district"],
  },
  {
    id: "bridge-timeline",
    kind: "bridge",
    bounds: { minX: -1.5, maxX: 1.5, minZ: 5.5, maxZ: 12.5 },
    connects: ["command-center", "timeline"],
  },
  {
    id: "bridge-build",
    kind: "bridge",
    bounds: { minX: -6.5, maxX: -3.5, minZ: -11.5, maxZ: -5.5 },
    connects: ["command-center", "build-lab"],
  },
  {
    id: "bridge-automation",
    kind: "bridge",
    bounds: { minX: 3.5, maxX: 6.5, minZ: -11.5, maxZ: -5.5 },
    connects: ["command-center", "automation-lab"],
  },
] as const;

export const WALKABLE_AREAS: readonly WalkableArea[] = [
  ...ZONES.map((zone) => ({
    id: `zone-${zone.id}`,
    kind: "zone" as const,
    bounds: zone.bounds,
    zoneId: zone.id,
  })),
  ...BRIDGES,
];

export const WALKABLE_BOUNDS = WALKABLE_AREAS.map((area) => area.bounds);

export const WORLD_EXTENTS: WorldBounds = {
  minX: Math.min(...WALKABLE_BOUNDS.map((area) => area.minX)),
  maxX: Math.max(...WALKABLE_BOUNDS.map((area) => area.maxX)),
  minZ: Math.min(...WALKABLE_BOUNDS.map((area) => area.minZ)),
  maxZ: Math.max(...WALKABLE_BOUNDS.map((area) => area.maxZ)),
};

export function constrainToWalkableWorld(point: Point2): Point2 {
  return constrainPointToAreas(point, WALKABLE_BOUNDS);
}

export function isWalkablePoint(point: Point2): boolean {
  return WALKABLE_BOUNDS.some((bounds) => pointInBounds(point, bounds));
}

export function zoneAtPoint(point: Point2): ZoneId | null {
  const zone = ZONES.find((candidate) => pointInBounds(point, candidate.bounds));
  return zone?.id ?? null;
}

export function overlaps(a: WorldBounds, b: WorldBounds): boolean {
  return !(
    a.maxX < b.minX ||
    a.minX > b.maxX ||
    a.maxZ < b.minZ ||
    a.minZ > b.maxZ
  );
}

export function districtConnections(): ReadonlyMap<ZoneId, readonly ZoneId[]> {
  const graph = new Map<ZoneId, ZoneId[]>();
  for (const zone of ZONES) graph.set(zone.id, []);

  for (const bridge of BRIDGES) {
    if (!bridge.connects) continue;
    const [left, right] = bridge.connects;
    graph.get(left)!.push(right);
    graph.get(right)!.push(left);
  }

  return graph;
}

export function reachableZones(start: ZoneId): Set<ZoneId> {
  const graph = districtConnections();
  const visited = new Set<ZoneId>();
  const queue: ZoneId[] = [start];

  while (queue.length > 0) {
    const current = queue.shift()!;
    if (visited.has(current)) continue;
    visited.add(current);
    for (const next of graph.get(current) ?? []) {
      if (!visited.has(next)) queue.push(next);
    }
  }

  return visited;
}
