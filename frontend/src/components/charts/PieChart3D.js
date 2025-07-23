import React, { useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

const PieSlice = ({ 
  position, 
  rotation, 
  color, 
  startAngle, 
  endAngle, 
  radius = 3, 
  height = 0.5,
  label,
  value,
  onHover,
  onLeave 
}) => {
  const meshRef = React.useRef();
  const [hovered, setHovered] = React.useState(false);

  useFrame(() => {
    if (meshRef.current && hovered) {
      meshRef.current.position.y = THREE.MathUtils.lerp(
        meshRef.current.position.y,
        0.2,
        0.1
      );
    } else if (meshRef.current) {
      meshRef.current.position.y = THREE.MathUtils.lerp(
        meshRef.current.position.y,
        0,
        0.1
      );
    }
  });

  const geometry = useMemo(() => {
    const shape = new THREE.Shape();
    const angle = endAngle - startAngle;
    
    shape.moveTo(0, 0);
    shape.absarc(0, 0, radius, startAngle, endAngle, false);
    shape.lineTo(0, 0);
    
    return new THREE.ExtrudeGeometry(shape, {
      depth: height,
      bevelEnabled: false
    });
  }, [startAngle, endAngle, radius, height]);

  return (
    <group position={position} rotation={rotation}>
      <mesh
        ref={meshRef}
        geometry={geometry}
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
        <meshStandardMaterial 
          color={hovered ? new THREE.Color(color).multiplyScalar(1.2) : color}
          transparent
          opacity={0.9}
        />
      </mesh>
    </group>
  );
};

const PieChart3D = ({ data = [], title = "3D Pie Chart", config = {} }) => {
  const [hoveredItem, setHoveredItem] = React.useState(null);

  const processedData = useMemo(() => {
    if (!data || data.length === 0) return [];
    
    const total = data.reduce((sum, item) => sum + (item.value || 0), 0);
    let currentAngle = 0;
    
    return data.map((item, index) => {
      const percentage = (item.value || 0) / total;
      const angle = percentage * Math.PI * 2;
      
      const slice = {
        ...item,
        startAngle: currentAngle,
        endAngle: currentAngle + angle,
        percentage: percentage * 100,
        color: item.color || `hsl(${index * 40}, 70%, 50%)`
      };
      
      currentAngle += angle;
      return slice;
    });
  }, [data]);

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
        No data available for pie chart
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <Canvas
        camera={{ position: [0, 8, 10], fov: 60 }}
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
          maxDistance={20}
        />

        {processedData.map((slice, index) => (
          <PieSlice
            key={`slice-${index}`}
            position={[0, 0, 0]}
            rotation={[-Math.PI / 2, 0, 0]}
            startAngle={slice.startAngle}
            endAngle={slice.endAngle}
            color={slice.color}
            label={slice.label}
            value={slice.value}
            onHover={setHoveredItem}
            onLeave={() => setHoveredItem(null)}
          />
        ))}

        <Text
          position={[0, 4, 0]}
          fontSize={0.8}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {title}
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
          <div>Percentage: {((hoveredItem.value / data.reduce((sum, item) => sum + item.value, 0)) * 100).toFixed(1)}%</div>
        </div>
      )}
    </div>
  );
};

export default PieChart3D;
