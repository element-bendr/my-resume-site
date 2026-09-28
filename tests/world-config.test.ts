import { describe, expect, it } from "vitest";
import projectsData from "../src/content/projects.json";
import {
  COMMAND_CENTER_BOUNDS,
  PLAYER_SPAWN,
  STATIONS,
} from "../src/world/world-config";
import { clampPoint } from "../src/world/movement";

describe("command-center world contract", () => {
  it("contains exactly three distinct interaction stations", () => {
    expect(STATIONS).toHaveLength(3);
    expect(new Set(STATIONS.map((station) => station.id)).size).toBe(3);
  });

  it("keeps spawn and every interaction point inside legal bounds", () => {
    expect(clampPoint(PLAYER_SPAWN, COMMAND_CENTER_BOUNDS)).toEqual(PLAYER_SPAWN);
    for (const station of STATIONS) {
      expect(clampPoint(station.interactionPoint, COMMAND_CENTER_BOUNDS)).toEqual(
        station.interactionPoint,
      );
    }
  });

  it("links project stations only to source-backed project records", () => {
    const projectIds = new Set(projectsData.map((project) => project.id));
    for (const station of STATIONS) {
      if (station.kind === "project") expect(projectIds.has(station.projectId ?? "")).toBe(true);
    }
  });
});
