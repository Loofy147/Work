import React, { useState, Suspense, useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import './App.css';

function Model({ geometry, stressData }) {
  const coloredGeometry = useMemo(() => {
    if (!geometry || !stressData) return null;

    const newGeometry = geometry.clone();
    const colors = [];
    const color = new THREE.Color();
    const maxStress = Math.max(...stressData);

    for (let i = 0; i < stressData.length; i++) {
        const stress = stressData[i];
        const normalizedStress = stress / maxStress;
        color.setHSL(0.7 * (1 - normalizedStress), 1, 0.5);
        colors.push(color.r, color.g, color.b);
    }

    newGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    return newGeometry;
  }, [geometry, stressData]);

  return (
    <mesh geometry={coloredGeometry}>
      <meshStandardMaterial vertexColors />
    </mesh>
  );
}

function App() {
  const [prompt, setPrompt] = useState('a long, thin beam');
  const [modelData, setModelData] = useState(null);

  const parsePromptAndGenerate = () => {
    // 1. Simple NLP with regex
    let length = 10, width = 2, height = 2; // Defaults
    if (prompt.includes('long')) length = 20;
    if (prompt.includes('short')) length = 5;
    if (prompt.includes('wide')) width = 4;
    if (prompt.includes('narrow')) width = 1;
    if (prompt.includes('tall')) height = 4;
    if (prompt.includes('flat')) height = 1;

    // 2. Procedural generation
    const geometry = new THREE.BoxGeometry(length, width, height, 10, 10, 10);

    // 3. Pseudo-simulation
    const vertices = geometry.attributes.position.array;
    const stress = [];
    for (let i = 0; i < vertices.length; i += 3) {
      // Stress = (distance from fixed end)^2
      stress.push((vertices[i] + length / 2) ** 2);
    }

    setModelData({ geometry, stressData: stress });
  };

  return (
    <div className="App">
      <div className="controls">
        <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        <button onClick={parsePromptAndGenerate}>Generate and Analyze</button>
      </div>
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <Suspense fallback={null}>
          {modelData && <Model geometry={modelData.geometry} stressData={modelData.stressData} />}
        </Suspense>
        <OrbitControls />
      </Canvas>
    </div>
  );
}

export default App;
