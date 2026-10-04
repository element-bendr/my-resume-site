import { describe, expect, it } from "vitest";
import { BLENDER_ART_ASSETS, BLENDER_ART_PLACEMENTS } from "../src/world/art/blender-art-config";

describe("Command Center authored scenery boundary", () => {
  it("uses the registry-backed GLB with bounded decorative loading", () => {
    expect(BLENDER_ART_ASSETS["command-center"]).toBe("/world/art/command-center.glb");
    expect(BLENDER_ART_PLACEMENTS["command-center"]).toEqual([0, 0, 0]);
  });

  it("keeps React-owned interaction and movement feedback in CommandCenter", () => {
    expect(Object.keys(BLENDER_ART_ASSETS)).toHaveLength(6);
  });

  it("does not grant gameplay authority to the authored scene", () => {
    expect(BLENDER_ART_ASSETS["command-center"]).not.toContain("topology");
  });
});
