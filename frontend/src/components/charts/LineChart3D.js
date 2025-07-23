import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Line } from '@react-three/drei';
import * as THREE from 'three';

const DataPoint = ({ position, color, label, value, onHover, onLeave }) => {
  const meshRef = useRef();
  const [hovered, setHovered] = React.useState(false);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(
        THREE.MathUtils.lerp(
          meshRef.current.scale.x,
          hovered ? 1.5 : 1,
          0.1
        )
      );
    }
  });

  return (
    <mesh
      ref={meshRef}
      position={position}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        onHover && onHover({ label, value });
      }}
      onPointerOut={(e) => {
        e.stopPropagation();
        setHovered(false);
        onLeave && onLeave();
      }}
    >
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial 
        color={hovered ? new THREE.Color(color).multiplyScalar(1.5) : color}
        emissive={hovered ? new THREE.Color(color).multiplyScalar(0.2) : new THREE.Color(0x000000)}
      />
    </mesh>
  );
};

const LineChart3D = ({ data = [], title = "3D Line Chart", config = {} }) => {
  const [hoveredItem, setHoveredItem] = React.useState(null);

  const processedData = useMemo(() => {
    if (!data || data.length === 0) return { points: [], linePoints: [] };

    const maxValue = Math.max(...data.map(item => item.value || 0));
    const spacing = 8 / Math.max(data.length - 1, 1);

    const points = data.map((item, index) => ({
      ...item,
      position: [
        (index - (data.length - 1) / 2) * spacing,
        ((item.value || 0) / maxValue) * 4,
        0
      ],
      normalizedValue: (item.value || 0) / maxValue,
      color: item.color || config.color || '#4CAF50'
    }));

    const linePoints = points.map(point => new THREE.Vector3(...point.position));

    return { points, linePoints };
  }, [data, config]);

  if (!data || data.length === 0) {
    return (
      <div style={{ 
        width: '100%', 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'linear-gradient(45deg, #1e1e1e, #2d2d2d)',
        color: 'white'
      }}>
        No data available for line chart
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <Canvas
        camera={{ position: [0, 5, 15], fov: 60 }}
        style={{ width: '100%', height: '100%' }}
      >
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} intensity={0.8} />
        <directionalLight position={[0, 10, 5]} intensity={0.5} />

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          maxPolarAngle={Math.PI / 2}
          minDistance={5}
          maxDistance={25}
        />

        {/* Line connecting points */}
        <Line
          points={processedData.linePoints}
          color={config.color || '#4CAF50'}
          lineWidth={3}
        />

        {/* Data points */}
        {processedData.points.map((point, index) => (
          <DataPoint
            key={`point-${index}`}
            position={point.position}
            color={point.color}
            label={point.label || `Point ${index + 1}`}
            value={point.value || 0}
            onHover={setHoveredItem}
            onLeave={() => setHoveredItem(null)}
          />
        ))}

        {/* Grid */}
        <gridHelper args={[20, 20, 0x404040, 0x404040]} position={[0, -0.1, 0]} />

        {/* Title */}
        <Text
          position={[0, 6, 0]}
          fontSize={0.8}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {title}
        </Text>

        {/* Axis labels */}
        <Text
          position={[0, -1, 0]}
          fontSize={0.4}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          Data Points
        </Text>
        
        <Text
          position={[-6, 2, 0]}
          fontSize={0.4}
          color="white"
          anchorX="center"
          anchorY="middle"
          rotation={[0, 0, Math.PI / 2]}
        >
          Values
        </Text>
      </Canvas>

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
            zIndex: 1000,
          }}
        >
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
            {hoveredItem.label}
          </div>
          <div>Value: {hoveredItem.value?.toLocaleString()}</div>
        </div>
      )}
    </div>
  );
};

export default LineChart3D;
