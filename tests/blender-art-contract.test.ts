import { describe, expect, it } from "vitest";
import { ZONES } from "../src/world/world-topology";
import {
  BLENDER_ART_ASSETS,
  BLENDER_ART_PLACEMENTS,
} from "../src/world/art/blender-art-config";

describe("Blender art contract", () => {
  it("declares exactly one GLB for every certified world zone", () => {
    const zoneIds = ZONES.map((zone) => zone.id).sort();
    expect(Object.keys(BLENDER_ART_ASSETS).sort()).toEqual(zoneIds);

    for (const zoneId of zoneIds) {
      expect(BLENDER_ART_ASSETS[zoneId]).toMatch(/^\/world\/art\/[a-z0-9-]+\.glb$/);
    }

    expect(new Set(Object.values(BLENDER_ART_ASSETS)).size).toBe(zoneIds.length);
  });

  it("anchors each authored scene at the center of its certified zone", () => {
    for (const zone of ZONES) {
      const [x, y, z] = BLENDER_ART_PLACEMENTS[zone.id];
      expect(y).toBe(0);
      expect(x).toBe((zone.bounds.minX + zone.bounds.maxX) / 2);
      expect(z).toBe((zone.bounds.minZ + zone.bounds.maxZ) / 2);
    }
  });
});
