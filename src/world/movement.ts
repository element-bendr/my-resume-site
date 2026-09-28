export interface Point2 {
  x: number;
  z: number;
}

export interface WorldBounds {
  minX: number;
  maxX: number;
  minZ: number;
  maxZ: number;
}

export interface StepResult {
  point: Point2;
  reached: boolean;
}

const EPSILON = 1e-8;

export function clampPoint(point: Point2, bounds: WorldBounds): Point2 {
  return {
    x: Math.min(bounds.maxX, Math.max(bounds.minX, point.x)),
    z: Math.min(bounds.maxZ, Math.max(bounds.minZ, point.z)),
  };
}

export function distanceSquared(a: Point2, b: Point2): number {
  const dx = a.x - b.x;
  const dz = a.z - b.z;
  return dx * dx + dz * dz;
}

export function stepToward(current: Point2, target: Point2, maxDistance: number): StepResult {
  if (maxDistance <= 0) return { point: current, reached: distanceSquared(current, target) <= EPSILON };

  const dx = target.x - current.x;
  const dz = target.z - current.z;
  const distance = Math.hypot(dx, dz);

  if (distance <= maxDistance || distance <= EPSILON) {
    return { point: { ...target }, reached: true };
  }

  const scale = maxDistance / distance;
  return {
    point: {
      x: current.x + dx * scale,
      z: current.z + dz * scale,
    },
    reached: false,
  };
}

export function cameraRelativeDirection(
  forwardAmount: number,
  rightAmount: number,
  cameraForward: Point2,
): Point2 {
  const length = Math.hypot(cameraForward.x, cameraForward.z);
  if (length <= EPSILON) return { x: 0, z: 0 };

  const forward = {
    x: cameraForward.x / length,
    z: cameraForward.z / length,
  };
  const right = {
    x: -forward.z,
    z: forward.x,
  };

  const x = forward.x * forwardAmount + right.x * rightAmount;
  const z = forward.z * forwardAmount + right.z * rightAmount;
  const intentLength = Math.hypot(x, z);

  if (intentLength <= EPSILON) return { x: 0, z: 0 };
  return { x: x / intentLength, z: z / intentLength };
}

export function withinRadius(a: Point2, b: Point2, radius: number): boolean {
  return distanceSquared(a, b) <= radius * radius;
}
