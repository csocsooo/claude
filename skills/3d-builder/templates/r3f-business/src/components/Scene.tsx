import { Canvas, useFrame } from '@react-three/fiber'
import { Environment, Float, OrbitControls } from '@react-three/drei'
import { Suspense, useRef } from 'react'
import type { Mesh } from 'three'

// Default fallback object — Claude: replace with <Model /> after running
// `bash skills/3d-builder/scripts/fetch-cc0-model.sh <url> ./public/model.glb`
// then `npx gltfjsx public/model.glb -o src/components/Model.tsx -t`.
function HeroObject() {
  const ref = useRef<Mesh>(null)
  useFrame((_, dt) => {
    if (ref.current) ref.current.rotation.y += dt * 0.3
  })
  return (
    <Float speed={1} rotationIntensity={0.3} floatIntensity={0.6}>
      <mesh ref={ref} castShadow receiveShadow>
        <icosahedronGeometry args={[1.3, 0]} />
        <meshStandardMaterial
          color="#__BRAND_500__"
          metalness={0.5}
          roughness={0.25}
        />
      </mesh>
    </Float>
  )
}

export default function Scene() {
  return (
    <Canvas
      shadows
      camera={{ position: [0, 0.4, 5], fov: 42 }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
    >
      <ambientLight intensity={0.35} />
      <directionalLight position={[5, 6, 5]} intensity={1.1} castShadow />
      <Suspense fallback={null}>
        <HeroObject />
        <Environment preset="city" />
      </Suspense>
      <OrbitControls
        enableZoom={false}
        enablePan={false}
        autoRotate
        autoRotateSpeed={0.6}
      />
    </Canvas>
  )
}
