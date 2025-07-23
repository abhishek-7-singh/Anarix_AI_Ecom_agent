import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

const Chart3D = ({ data, chartType, title, config }) => {
  return (
    <Canvas
      camera={{ position: [0, 5, 15], fov: 60 }}
      style={{ width: '100%', height: '100%' }}
    >
      <ambientLight intensity={0.6} />
      <pointLight position={[10, 10, 10]} intensity={0.8} />
      <OrbitControls enableDamping dampingFactor={0.05} />
      
      <mesh>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="orange" />
      </mesh>
    </Canvas>
  );
};

export default Chart3D;
