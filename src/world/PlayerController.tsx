import { useFrame, useThree } from "@react-three/fiber";
import { useEffect, useRef } from "react";
import { Group, Vector3 } from "three";
import type { OptionalVectorRef, StationRef, VectorRef } from "./WorldEntry";
import {
  BRISK_WALK_SPEED,
  CLICK_WALK_SPEED,
  COMMAND_CENTER_BOUNDS,
  INTERACTION_RADIUS,
  STATIONS,
  TARGET_EPSILON,
  WALK_ACCELERATION_SECONDS,
  WALK_SPEED,
  type StationId,
} from "./world-config";
import {
  cameraRelativeDirection,
  clampPoint,
  distanceSquared,
  stepToward,
  withinRadius,
} from "./movement";

interface PlayerControllerProps {
  playerPosition: VectorRef;
  movementTarget: OptionalVectorRef;
  pendingInteraction: StationRef;
  controlsEnabled: boolean;
  onInteract: (station: StationId) => void;
  onNearestChange: (station: StationId | null) => void;
}

const MOVEMENT_KEYS = new Set([
  "KeyW",
  "KeyA",
  "KeyS",
  "KeyD",
  "ArrowUp",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
]);

export function PlayerController({
  playerPosition,
  movementTarget,
  pendingInteraction,
  controlsEnabled,
  onInteract,
  onNearestChange,
}: PlayerControllerProps) {
  const avatar = useRef<Group>(null);
  const pressed = useRef(new Set<string>());
  const interactionRequested = useRef(false);
  const heldSeconds = useRef(0);
  const nearestRef = useRef<StationId | null>(null);
  const camera = useThree((state) => state.camera);
  const cameraForward = useRef(new Vector3());
  const walking = useRef(false);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (!controlsEnabled) return;
      if (MOVEMENT_KEYS.has(event.code)) {
        event.preventDefault();
        pressed.current.add(event.code);
      }
      if (event.code === "KeyE") {
        event.preventDefault();
        interactionRequested.current = true;
      }
    };

    const onKeyUp = (event: KeyboardEvent) => {
      pressed.current.delete(event.code);
    };

    window.addEventListener("keydown", onKeyDown, { passive: false });
    window.addEventListener("keyup", onKeyUp);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
    };
  }, [controlsEnabled]);

  useEffect(() => {
    if (controlsEnabled) return;
    pressed.current.clear();
    heldSeconds.current = 0;
    walking.current = false;
  }, [controlsEnabled]);

  useFrame((state, delta) => {
    const position = playerPosition.current;
    let movedX = 0;
    let movedZ = 0;
    let isWalking = false;

    if (controlsEnabled) {
      const forwardAmount =
        Number(pressed.current.has("KeyW") || pressed.current.has("ArrowUp")) -
        Number(pressed.current.has("KeyS") || pressed.current.has("ArrowDown"));
      const rightAmount =
        Number(pressed.current.has("KeyD") || pressed.current.has("ArrowRight")) -
        Number(pressed.current.has("KeyA") || pressed.current.has("ArrowLeft"));

      if (forwardAmount !== 0 || rightAmount !== 0) {
        movementTarget.current = null;
        pendingInteraction.current = null;
        camera.getWorldDirection(cameraForward.current);
        const direction = cameraRelativeDirection(forwardAmount, rightAmount, {
          x: cameraForward.current.x,
          z: cameraForward.current.z,
        });
        heldSeconds.current += delta;
        const acceleration = Math.min(1, heldSeconds.current / WALK_ACCELERATION_SECONDS);
        const speed = WALK_SPEED + (BRISK_WALK_SPEED - WALK_SPEED) * acceleration;
        const next = clampPoint(
          {
            x: position.x + direction.x * speed * delta,
            z: position.z + direction.z * speed * delta,
          },
          COMMAND_CENTER_BOUNDS,
        );
        movedX = next.x - position.x;
        movedZ = next.z - position.z;
        position.set(next.x, 0, next.z);
        isWalking = Math.abs(movedX) + Math.abs(movedZ) > 0.0001;
      } else {
        heldSeconds.current = 0;
        const target = movementTarget.current;
        if (target) {
          const result = stepToward(
            { x: position.x, z: position.z },
            { x: target.x, z: target.z },
            CLICK_WALK_SPEED * delta,
          );
          const next = clampPoint(result.point, COMMAND_CENTER_BOUNDS);
          movedX = next.x - position.x;
          movedZ = next.z - position.z;
          position.set(next.x, 0, next.z);
          isWalking = !result.reached || Math.hypot(movedX, movedZ) > TARGET_EPSILON;

          if (result.reached) {
            movementTarget.current = null;
            const pending = pendingInteraction.current;
            pendingInteraction.current = null;
            if (
              pending &&
              withinRadius(
                { x: position.x, z: position.z },
                STATIONS.find((station) => station.id === pending)!.interactionPoint,
                INTERACTION_RADIUS,
              )
            ) {
              onInteract(pending);
            }
          }
        }
      }
    }

    walking.current = isWalking;

    if (avatar.current) {
      const bob = isWalking ? Math.sin(state.clock.elapsedTime * 9) * 0.035 : 0;
      avatar.current.position.set(position.x, bob, position.z);
      if (Math.abs(movedX) + Math.abs(movedZ) > 0.0001) {
        avatar.current.rotation.y = Math.atan2(movedX, movedZ);
      }
    }

    let nearest: StationId | null = null;
    let bestDistance = Number.POSITIVE_INFINITY;
    for (const station of STATIONS) {
      const squared = distanceSquared(
        { x: position.x, z: position.z },
        station.interactionPoint,
      );
      if (squared <= INTERACTION_RADIUS * INTERACTION_RADIUS && squared < bestDistance) {
        bestDistance = squared;
        nearest = station.id;
      }
    }

    if (nearestRef.current !== nearest) {
      nearestRef.current = nearest;
      onNearestChange(nearest);
    }

    if (interactionRequested.current) {
      interactionRequested.current = false;
      if (controlsEnabled && nearest) onInteract(nearest);
    }
  });

  return (
    <group ref={avatar} position={[playerPosition.current.x, 0, playerPosition.current.z]}>
      <mesh position={[-0.14, 0.28, 0]}>
        <boxGeometry args={[0.18, 0.55, 0.22]} />
        <meshStandardMaterial color="#163552" />
      </mesh>
      <mesh position={[0.14, 0.28, 0]}>
        <boxGeometry args={[0.18, 0.55, 0.22]} />
        <meshStandardMaterial color="#163552" />
      </mesh>
      <mesh position={[0, 0.78, 0]}>
        <cylinderGeometry args={[0.3, 0.36, 0.72, 8]} />
        <meshStandardMaterial color="#2d5d82" metalness={0.18} roughness={0.55} />
      </mesh>
      <mesh position={[0, 1.28, 0]}>
        <sphereGeometry args={[0.27, 16, 12]} />
        <meshStandardMaterial color="#d6e6f3" roughness={0.7} />
      </mesh>
      <mesh position={[0, 1.28, 0.235]}>
        <boxGeometry args={[0.28, 0.08, 0.035]} />
        <meshStandardMaterial color="#63d8ff" emissive="#2fa7d4" emissiveIntensity={1.2} />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.018, 0]}>
        <ringGeometry args={[0.38, 0.43, 24]} />
        <meshBasicMaterial color="#63d8ff" transparent opacity={0.45} />
      </mesh>
    </group>
  );
}
