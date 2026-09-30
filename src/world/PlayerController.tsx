import { useFrame, useThree } from "@react-three/fiber";
import { useEffect, useRef } from "react";
import { Group, Vector3 } from "three";
import type { OptionalVectorRef, StationRef, VectorRef } from "./WorldEntry";
import {
  BRISK_WALK_SPEED,
  CLICK_WALK_SPEED,
  INTERACTION_RADIUS,
  STATIONS,
  TARGET_EPSILON,
  WALK_ACCELERATION_SECONDS,
  WALK_SPEED,
  type StationId,
} from "./world-config";
import {
  cameraRelativeDirection,
  distanceSquared,
  stepToward,
  withinRadius,
} from "./movement";
import {
  constrainToWalkableWorld,
  zoneAtPoint,
  type ZoneId,
} from "./world-topology";

interface PlayerControllerProps {
  playerPosition: VectorRef;
  movementTarget: OptionalVectorRef;
  pendingInteraction: StationRef;
  controlsEnabled: boolean;
  onInteract: (station: StationId) => void;
  onNearestChange: (station: StationId | null) => void;
  onZoneChange: (zone: ZoneId) => void;
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
  onZoneChange,
}: PlayerControllerProps) {
  const avatar = useRef<Group>(null);
  const leftArm = useRef<Group>(null);
  const rightArm = useRef<Group>(null);
  const leftLeg = useRef<Group>(null);
  const rightLeg = useRef<Group>(null);
  const pressed = useRef(new Set<string>());
  const interactionRequested = useRef(false);
  const heldSeconds = useRef(0);
  const nearestRef = useRef<StationId | null>(null);
  const zoneRef = useRef<ZoneId>("command-center");
  const camera = useThree((state) => state.camera);
  const cameraForward = useRef(new Vector3());

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
        const next = constrainToWalkableWorld({
          x: position.x + direction.x * speed * delta,
          z: position.z + direction.z * speed * delta,
        });
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
          const next = constrainToWalkableWorld(result.point);
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

    if (avatar.current) {
      const gait = Math.sin(state.clock.elapsedTime * 8.5);
      const bob = isWalking ? Math.abs(gait) * 0.045 : 0;
      avatar.current.position.set(position.x, bob, position.z);
      if (Math.abs(movedX) + Math.abs(movedZ) > 0.0001) {
        avatar.current.rotation.y = Math.atan2(movedX, movedZ);
      }

      const armSwing = isWalking ? gait * 0.48 : 0;
      const legSwing = isWalking ? gait * 0.58 : 0;
      if (leftArm.current) leftArm.current.rotation.x = armSwing;
      if (rightArm.current) rightArm.current.rotation.x = -armSwing;
      if (leftLeg.current) leftLeg.current.rotation.x = -legSwing;
      if (rightLeg.current) rightLeg.current.rotation.x = legSwing;
    }

    const zone = zoneAtPoint({ x: position.x, z: position.z });
    if (zone && zoneRef.current !== zone) {
      zoneRef.current = zone;
      onZoneChange(zone);
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
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.018, 0]}>
        <ringGeometry args={[0.4, 0.47, 28]} />
        <meshBasicMaterial color="#63d8ff" transparent opacity={0.34} />
      </mesh>

      <group ref={leftLeg} position={[-0.17, 0.66, 0]}>
        <mesh position={[0, -0.28, 0]}>
          <boxGeometry args={[0.22, 0.58, 0.28]} />
          <meshStandardMaterial color="#151c2a" roughness={0.72} />
        </mesh>
        <mesh position={[0, -0.59, 0.07]}>
          <boxGeometry args={[0.26, 0.12, 0.42]} />
          <meshStandardMaterial color="#0b1019" roughness={0.8} />
        </mesh>
      </group>

      <group ref={rightLeg} position={[0.17, 0.66, 0]}>
        <mesh position={[0, -0.28, 0]}>
          <boxGeometry args={[0.22, 0.58, 0.28]} />
          <meshStandardMaterial color="#151c2a" roughness={0.72} />
        </mesh>
        <mesh position={[0, -0.59, 0.07]}>
          <boxGeometry args={[0.26, 0.12, 0.42]} />
          <meshStandardMaterial color="#0b1019" roughness={0.8} />
        </mesh>
      </group>

      <mesh castShadow position={[0, 1.06, 0]}>
        <boxGeometry args={[0.68, 0.76, 0.36]} />
        <meshStandardMaterial color="#202b3b" metalness={0.08} roughness={0.68} />
      </mesh>
      <mesh position={[0, 1.12, 0.19]}>
        <boxGeometry args={[0.5, 0.42, 0.025]} />
        <meshStandardMaterial color="#26374c" roughness={0.5} />
      </mesh>
      <mesh position={[0, 1.18, -0.25]}>
        <boxGeometry args={[0.48, 0.6, 0.2]} />
        <meshStandardMaterial color="#111923" metalness={0.2} roughness={0.58} />
      </mesh>
      <mesh position={[0, 1.2, -0.36]}>
        <boxGeometry args={[0.08, 0.28, 0.025]} />
        <meshStandardMaterial
          color="#9aeaff"
          emissive="#39bfff"
          emissiveIntensity={1.7}
          toneMapped={false}
        />
      </mesh>

      <group ref={leftArm} position={[-0.46, 1.28, 0]}>
        <mesh position={[0, -0.28, 0]}>
          <capsuleGeometry args={[0.105, 0.42, 4, 8]} />
          <meshStandardMaterial color="#202b3b" roughness={0.68} />
        </mesh>
        <mesh position={[0, -0.57, 0.02]}>
          <sphereGeometry args={[0.115, 10, 8]} />
          <meshStandardMaterial color="#b9876f" roughness={0.82} />
        </mesh>
      </group>

      <group ref={rightArm} position={[0.46, 1.28, 0]}>
        <mesh position={[0, -0.28, 0]}>
          <capsuleGeometry args={[0.105, 0.42, 4, 8]} />
          <meshStandardMaterial color="#202b3b" roughness={0.68} />
        </mesh>
        <mesh position={[0, -0.57, 0.02]}>
          <sphereGeometry args={[0.115, 10, 8]} />
          <meshStandardMaterial color="#b9876f" roughness={0.82} />
        </mesh>
      </group>

      <mesh castShadow position={[0, 1.66, 0]}>
        <sphereGeometry args={[0.28, 18, 14]} />
        <meshStandardMaterial color="#b9876f" roughness={0.82} />
      </mesh>
      <mesh position={[0, 1.82, -0.02]} scale={[1.04, 0.62, 1.02]}>
        <dodecahedronGeometry args={[0.29, 0]} />
        <meshStandardMaterial color="#10141d" roughness={0.86} />
      </mesh>
      <mesh position={[0, 1.65, 0.265]}>
        <boxGeometry args={[0.29, 0.055, 0.025]} />
        <meshStandardMaterial
          color="#bfefff"
          emissive="#55cfff"
          emissiveIntensity={1.05}
          toneMapped={false}
        />
      </mesh>
    </group>
  );
}
