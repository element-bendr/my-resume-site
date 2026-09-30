import { Sky } from "@react-three/drei";

const RIDGE_POINTS = [
  [-34, -18, 1.8, 8.5],
  [-27, -27, 2.2, 11],
  [-16, -36, 1.5, 7.5],
  [18, -38, 1.8, 9],
  [30, -28, 2.4, 12],
  [38, -14, 1.7, 8],
  [-39, 16, 1.6, 8],
  [37, 18, 2, 10],
] as const;

function DistantBackdrop() {
  return (
    <group position={[0, -7.5, 0]}>
      {RIDGE_POINTS.map(([x, z, radius, height], index) => (
        <group key={index} position={[x, 0, z]}>
          <mesh rotation={[0, index * 0.61, 0]}>
            <coneGeometry args={[radius * 3.2, height, 7]} />
            <meshStandardMaterial color="#17213a" roughness={0.96} />
          </mesh>
          <mesh position={[0, height * 0.34, 0]} rotation={[0, index * 0.37, 0]}>
            <coneGeometry args={[radius * 1.8, height * 0.58, 6]} />
            <meshStandardMaterial color="#283253" roughness={0.92} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

export function WorldEnvironment() {
  return (
    <>
      <color attach="background" args={["#10182d"]} />
      <fog attach="fog" args={["#111a33", 34, 82]} />

      <Sky
        distance={450000}
        sunPosition={[18, -4, -24]}
        turbidity={10}
        rayleigh={0.2}
        mieCoefficient={0.02}
        mieDirectionalG={0.72}
      />

      <hemisphereLight args={["#b8d9ff", "#241d35", 1.45]} />
      <ambientLight intensity={0.24} />
      <directionalLight
        castShadow
        position={[16, 22, 10]}
        intensity={2.3}
        color="#ffd5a2"
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-near={1}
        shadow-camera-far={70}
        shadow-camera-left={-32}
        shadow-camera-right={32}
        shadow-camera-top={32}
        shadow-camera-bottom={-32}
      />
      <directionalLight position={[-18, 8, -12]} intensity={0.55} color="#7fb5ff" />

      <DistantBackdrop />
    </>
  );
}
