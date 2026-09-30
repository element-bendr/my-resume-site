import { describe, expect, it } from "vitest";
import experienceData from "../src/content/experience.json";
import hobbiesData from "../src/content/hobbies.json";
import projectsData from "../src/content/projects.json";
import {
  PLAYER_SPAWN,
  STATIONS,
  stationsForZone,
} from "../src/world/world-config";
import {
  isWalkablePoint,
  zoneAtPoint,
} from "../src/world/world-topology";

describe("world interaction registry", () => {
  it("keeps every station id unique and visibly labelled", () => {
    expect(STATIONS.length).toBeGreaterThanOrEqual(19);
    expect(new Set(STATIONS.map((station) => station.id)).size).toBe(STATIONS.length);
    for (const station of STATIONS) {
      expect(station.shortLabel.trim().length).toBeGreaterThan(0);
      expect(isWalkablePoint(station.interactionPoint)).toBe(true);
      expect(zoneAtPoint(station.interactionPoint)).toBe(station.zoneId);
    }
  });

  it("keeps the original spawn in the Command Center", () => {
    expect(zoneAtPoint(PLAYER_SPAWN)).toBe("command-center");
  });

  it("keeps project stations source-backed", () => {
    const ids = new Set(projectsData.map((project) => project.id));
    for (const station of STATIONS.filter((item) => item.kind === "project")) {
      expect(ids.has(station.projectId ?? "")).toBe(true);
    }
  });

  it("keeps timeline stations tied to structured experience", () => {
    const ids = new Set(experienceData.map((entry) => entry.id));
    for (const station of STATIONS.filter((item) => item.kind === "experience")) {
      expect(ids.has(station.experienceId ?? "")).toBe(true);
    }
  });

  it("keeps hobby stations tied only to user-approved hobby records", () => {
    const ids = new Set(hobbiesData.map((entry) => entry.id));
    for (const station of STATIONS.filter((item) => item.kind === "hobby")) {
      expect(ids.has(station.hobbyId ?? "")).toBe(true);
    }
  });

  it("keeps Ask in the Command Center and project detail in districts", () => {
    expect(stationsForZone("command-center").map((station) => station.id)).toEqual(["ask-terminal"]);
    expect(stationsForZone("build-lab").length).toBeGreaterThan(0);
    expect(stationsForZone("automation-lab").length).toBeGreaterThan(0);
    expect(stationsForZone("client-street").length).toBeGreaterThan(0);
  });
});
