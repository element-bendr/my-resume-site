import type { Point2 } from "./movement";
import { COMMAND_CENTER_BOUNDS, type ZoneId } from "./world-topology";

export type StationId =
  | "ask-terminal"
  | "build-memory-os"
  | "build-mnemos"
  | "build-palimpsest"
  | "automation-pcas"
  | "automation-newsharness"
  | "automation-chronoquill"
  | "automation-artsports"
  | "automation-governed-runtime"
  | "client-trifecta"
  | "client-steelmade"
  | "timeline-vinfinity"
  | "timeline-hcl"
  | "timeline-niit"
  | "hobby-gaming"
  | "hobby-anime"
  | "hobby-kettlebells"
  | "hobby-philosophy"
  | "hobby-tinkering";

export type StationKind = "project" | "ask" | "experience" | "hobby";

export interface StationConfig {
  id: StationId;
  title: string;
  shortLabel: string;
  kind: StationKind;
  zoneId: ZoneId;
  projectId?: string;
  experienceId?: string;
  hobbyId?: string;
  position: readonly [number, number, number];
  interactionPoint: Point2;
  accent: string;
}

export { COMMAND_CENTER_BOUNDS };

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
    id: "ask-terminal",
    title: "Ask Terminal",
    shortLabel: "Ask",
    kind: "ask",
    zoneId: "command-center",
    position: [4.35, 0, -2.7],
    interactionPoint: { x: 3.55, z: -1.45 },
    accent: "#75f2c8",
  },
  {
    id: "build-memory-os",
    title: "Memory OS Vault",
    shortLabel: "Memory OS",
    kind: "project",
    zoneId: "build-lab",
    projectId: "memory-os",
    position: [-13, 0, -17],
    interactionPoint: { x: -12.2, z: -15.7 },
    accent: "#9a8cff",
  },
  {
    id: "build-mnemos",
    title: "Mnemos Review Chamber",
    shortLabel: "Mnemos",
    kind: "project",
    zoneId: "build-lab",
    projectId: "mnemos",
    position: [-9, 0, -18.7],
    interactionPoint: { x: -9, z: -17.15 },
    accent: "#c19cff",
  },
  {
    id: "build-palimpsest",
    title: "Palimpsest Archive",
    shortLabel: "Palimpsest",
    kind: "project",
    zoneId: "build-lab",
    projectId: "palimpsest",
    position: [-5, 0, -17],
    interactionPoint: { x: -5.8, z: -15.7 },
    accent: "#7f8cff",
  },
  {
    id: "automation-pcas",
    title: "PCAS Opportunity Radar",
    shortLabel: "PCAS",
    kind: "project",
    zoneId: "automation-lab",
    projectId: "pcas",
    position: [5.1, 0, -17],
    interactionPoint: { x: 5.9, z: -15.7 },
    accent: "#75f2c8",
  },
  {
    id: "automation-newsharness",
    title: "Newsharness Signal Array",
    shortLabel: "Newsharness",
    kind: "project",
    zoneId: "automation-lab",
    projectId: "newsharness",
    position: [7.5, 0, -18.7],
    interactionPoint: { x: 7.5, z: -17.15 },
    accent: "#58d7ff",
  },
  {
    id: "automation-chronoquill",
    title: "ChronoQuill Scheduler",
    shortLabel: "ChronoQuill",
    kind: "project",
    zoneId: "automation-lab",
    projectId: "chronoquill",
    position: [10, 0, -17],
    interactionPoint: { x: 10, z: -15.7 },
    accent: "#5ee5b5",
  },
  {
    id: "automation-artsports",
    title: "ArtSports Content OS",
    shortLabel: "Content OS",
    kind: "project",
    zoneId: "automation-lab",
    projectId: "artsports-content-os",
    position: [12.5, 0, -18.7],
    interactionPoint: { x: 12.5, z: -17.15 },
    accent: "#74c8ff",
  },
  {
    id: "automation-governed-runtime",
    title: "Governed Runtime",
    shortLabel: "Runtime",
    kind: "project",
    zoneId: "automation-lab",
    projectId: "governed-runtime",
    position: [14, 0, -16.2],
    interactionPoint: { x: 13.2, z: -14.9 },
    accent: "#8bf5d0",
  },
  {
    id: "client-trifecta",
    title: "Trifecta / KPDC",
    shortLabel: "Trifecta",
    kind: "project",
    zoneId: "client-street",
    projectId: "trifecta-kpdc",
    position: [-19.3, 0, -2.3],
    interactionPoint: { x: -18.1, z: -1.5 },
    accent: "#ffb86b",
  },
  {
    id: "client-steelmade",
    title: "SteelMade",
    shortLabel: "SteelMade",
    kind: "project",
    zoneId: "client-street",
    projectId: "steelmade",
    position: [-15.2, 0, 2.1],
    interactionPoint: { x: -14.1, z: 1.3 },
    accent: "#ff8b6b",
  },
  {
    id: "timeline-vinfinity",
    title: "V-Infinity",
    shortLabel: "2014–Now",
    kind: "experience",
    zoneId: "timeline",
    experienceId: "vinfinity-ai-systems-architect",
    position: [-4.1, 0, 16.5],
    interactionPoint: { x: -4.1, z: 17.7 },
    accent: "#f4d06f",
  },
  {
    id: "timeline-hcl",
    title: "HCL Comnet",
    shortLabel: "2009–2013",
    kind: "experience",
    zoneId: "timeline",
    experienceId: "hcl-cybersecurity-incident-management",
    position: [0, 0, 17.3],
    interactionPoint: { x: 0, z: 18.5 },
    accent: "#e9c85d",
  },
  {
    id: "timeline-niit",
    title: "NIIT",
    shortLabel: "2007",
    kind: "experience",
    zoneId: "timeline",
    experienceId: "niit-elearning-content-development",
    position: [4.1, 0, 16.5],
    interactionPoint: { x: 4.1, z: 17.7 },
    accent: "#d9b84d",
  },
  {
    id: "hobby-gaming",
    title: "Gaming",
    shortLabel: "Gaming",
    kind: "hobby",
    zoneId: "hobby-district",
    hobbyId: "gaming",
    position: [14.3, 0, -2.7],
    interactionPoint: { x: 15.2, z: -1.6 },
    accent: "#ff7fcf",
  },
  {
    id: "hobby-anime",
    title: "Anime",
    shortLabel: "Anime",
    kind: "hobby",
    zoneId: "hobby-district",
    hobbyId: "anime",
    position: [17, 0, -3.2],
    interactionPoint: { x: 17, z: -1.7 },
    accent: "#ff9ddb",
  },
  {
    id: "hobby-kettlebells",
    title: "Kettlebells",
    shortLabel: "Kettlebells",
    kind: "hobby",
    zoneId: "hobby-district",
    hobbyId: "kettlebells",
    position: [19.7, 0, -2.7],
    interactionPoint: { x: 18.8, z: -1.6 },
    accent: "#ff6fb0",
  },
  {
    id: "hobby-philosophy",
    title: "Philosophy",
    shortLabel: "Philosophy",
    kind: "hobby",
    zoneId: "hobby-district",
    hobbyId: "philosophy",
    position: [15.5, 0, 2.4],
    interactionPoint: { x: 16.2, z: 1.25 },
    accent: "#d98cff",
  },
  {
    id: "hobby-tinkering",
    title: "Tinkering",
    shortLabel: "Tinkering",
    kind: "hobby",
    zoneId: "hobby-district",
    hobbyId: "tinkering",
    position: [19, 0, 2.4],
    interactionPoint: { x: 18.3, z: 1.25 },
    accent: "#ffb0e3",
  },
] as const;

export const STATION_BY_ID = Object.fromEntries(
  STATIONS.map((station) => [station.id, station]),
) as Record<StationId, StationConfig>;

export const stationsForZone = (zoneId: ZoneId) =>
  STATIONS.filter((station) => station.zoneId === zoneId);
