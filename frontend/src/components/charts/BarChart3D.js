import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

const Bar = ({ position, scale, color, label, value, onHover, onLeave }) => {
  const meshRef = useRef();
  const [hovered, setHovered] = React.useState(false);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.scale.y = THREE.MathUtils.lerp(
        meshRef.current.scale.y,
        hovered ? scale[1] * 1.1 : scale[1],
        0.1
      );
    }
  });

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        scale={scale}
        onPointerOver={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'pointer';
          setHovered(true);
          onHover && onHover({ label, value });
        }}
        onPointerOut={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'default';
          setHovered(false);
          onLeave && onLeave();
        }}
      >
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial 
          color={hovered ? new THREE.Color(color).multiplyScalar(1.2) : color}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      <Text
        position={[0, -scale[1] / 2 - 0.5, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        fontSize={0.3}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {label}
      </Text>
      
      <Text
        position={[0, scale[1] / 2 + 0.3, 0]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {typeof value === 'number' ? value.toLocaleString() : value}
      </Text>
    </group>
  );
};

const BarChart3D = ({ data = [], title = "3D Bar Chart", config = {} }) => {
  const [hoveredItem, setHoveredItem] = React.useState(null);

  const processedData = useMemo(() => {
    if (!data || data.length === 0) return [];

    const maxValue = Math.max(...data.map(item => item.value || 0));
    if (maxValue === 0) return []; // Prevent division by zero

    const spacing = 2;

    return data.slice(0, 20).map((item, index) => ({
      ...item,
      position: [(index - data.length / 2) * spacing, 0, 0],
      scale: [1.5, Math.max((item.value || 0) / maxValue * 5, 0.1), 1.5], // Minimum height
      normalizedValue: (item.value || 0) / maxValue,
    }));
  }, [data]);

  // Show loading state if no data
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        width: '100%', 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'linear-gradient(45deg, #1e1e1e, #2d2d2d)'
      }}>
        <div style={{ color: 'white', fontSize: '18px' }}>
          No data available for visualization
        </div>
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <Canvas
        camera={{ position: [0, 5, 15], fov: 60 }}
        style={{ width: '100%', height: '100%' }}
        gl={{ antialias: true, alpha: false }}
      >
        {/* Lighting setup */}
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} intensity={0.8} />
        <pointLight position={[-10, 10, -10]} intensity={0.4} />
        <directionalLight position={[0, 10, 5]} intensity={0.5} />

        {/* Camera controls */}
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          maxPolarAngle={Math.PI / 2}
          minDistance={5}
          maxDistance={50}
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
        />

        {/* Render bars */}
        {processedData.map((item, index) => (
          <Bar
            key={`bar-${index}-${item.label}`}
            position={item.position}
            scale={item.scale}
            color={item.color || config.colors?.[index % config.colors?.length] || `hsl(${index * 30}, 70%, 50%)`}
            label={item.label || `Item ${index + 1}`}
            value={item.value || 0}
            onHover={setHoveredItem}
            onLeave={() => setHoveredItem(null)}
          />
        ))}

        {/* Ground grid */}
        <gridHelper args={[30, 30, 0x404040, 0x404040]} position={[0, -0.1, 0]} />

        {/* Title */}
        <Text
          position={[0, 8, 0]}
          fontSize={0.8}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {title}
        </Text>
      </Canvas>

      {/* Hover tooltip */}
      {hoveredItem && (
        <div
          style={{
            position: 'absolute',
            top: '20px',
            left: '20px',
            background: 'rgba(0, 0, 0, 0.9)',
            color: 'white',
            padding: '12px 16px',
            borderRadius: '8px',
            fontSize: '14px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            zIndex: 1000,
          }}
        >
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
            {hoveredItem.label}
          </div>
          <div>Value: {hoveredItem.value?.toLocaleString() || 'N/A'}</div>
        </div>
      )}

      {/* Controls hint */}
      <div
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          background: 'rgba(0, 0, 0, 0.7)',
          color: 'white',
          padding: '8px 12px',
          borderRadius: '6px',
          fontSize: '12px',
          zIndex: 1000,
        }}
      >
        <div>🖱️ Drag to rotate</div>
        <div>🔍 Scroll to zoom</div>
        <div>👆 Hover bars for details</div>
      </div>
    </div>
  );
};

export default BarChart3D;
