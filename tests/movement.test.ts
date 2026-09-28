import { describe, expect, it } from "vitest";
import {
  cameraRelativeDirection,
  clampPoint,
  stepToward,
  withinRadius,
} from "../src/world/movement";
import { COMMAND_CENTER_BOUNDS } from "../src/world/world-config";

describe("command-center movement math", () => {
  it("clamps movement to legal world bounds", () => {
    expect(clampPoint({ x: 99, z: -99 }, COMMAND_CENTER_BOUNDS)).toEqual({ x: 8, z: -6 });
  });

  it("steps toward a target without overshooting", () => {
    const first = stepToward({ x: 0, z: 0 }, { x: 3, z: 4 }, 2);
    expect(first.reached).toBe(false);
    expect(first.point.x).toBeCloseTo(1.2);
    expect(first.point.z).toBeCloseTo(1.6);

    const final = stepToward(first.point, { x: 3, z: 4 }, 10);
    expect(final).toEqual({ point: { x: 3, z: 4 }, reached: true });
  });

  it("maps keyboard intent relative to the camera", () => {
    expect(cameraRelativeDirection(1, 0, { x: 0, z: -1 })).toEqual({ x: 0, z: -1 });
    expect(cameraRelativeDirection(0, 1, { x: 0, z: -1 })).toEqual({ x: 1, z: 0 });
  });

  it("uses squared distance for interaction reach", () => {
    expect(withinRadius({ x: 0, z: 0 }, { x: 1, z: 1 }, 1.5)).toBe(true);
    expect(withinRadius({ x: 0, z: 0 }, { x: 2, z: 0 }, 1.5)).toBe(false);
  });
});
