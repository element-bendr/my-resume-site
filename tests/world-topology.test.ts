import { describe, expect, it } from "vitest";
import {
  BRIDGES,
  ZONES,
  constrainToWalkableWorld,
  isWalkablePoint,
  overlaps,
  parseZoneId,
  reachableZones,
  zoneAtPoint,
} from "../src/world/world-topology";

describe("Portfolio World topology", () => {
  it("has one deterministic configuration for every major zone", () => {
    expect(ZONES.map((zone) => zone.id)).toEqual([
      "command-center",
      "client-street",
      "hobby-district",
      "timeline",
      "build-lab",
      "automation-lab",
    ]);
  });

  it("keeps every fast-travel spawn inside its own district", () => {
    for (const zone of ZONES) {
      expect(zoneAtPoint(zone.fastTravelPoint)).toBe(zone.id);
      expect(isWalkablePoint(zone.fastTravelPoint)).toBe(true);
    }
  });

  it("connects every district to the Command Center", () => {
    expect([...reachableZones("command-center")].sort()).toEqual(
      ZONES.map((zone) => zone.id).sort(),
    );
  });

  it("uses bridges that overlap both districts they connect", () => {
    const byId = new Map(ZONES.map((zone) => [zone.id, zone]));
    for (const bridge of BRIDGES) {
      const [left, right] = bridge.connects!;
      expect(overlaps(bridge.bounds, byId.get(left)!.bounds)).toBe(true);
      expect(overlaps(bridge.bounds, byId.get(right)!.bounds)).toBe(true);
    }
  });

  it("keeps legal points unchanged", () => {
    const point = { x: -17, z: 0 };
    expect(constrainToWalkableWorld(point)).toEqual(point);
  });

  it("projects void points to the nearest legal world boundary", () => {
    const projected = constrainToWalkableWorld({ x: -10, z: 8 });
    expect(isWalkablePoint(projected)).toBe(true);
    expect(projected).not.toEqual({ x: -10, z: 8 });
  });

  it("accepts only known zone ids for deep links", () => {
    expect(parseZoneId("automation-lab")).toBe("automation-lab");
    expect(parseZoneId("hobby-district")).toBe("hobby-district");
    expect(parseZoneId("moon-base")).toBeNull();
    expect(parseZoneId(null)).toBeNull();
  });
});
