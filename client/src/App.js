import React, { useState, Suspense, useMemo, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { InferenceSession, Tensor } from 'onnxruntime-web';
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
        const normalizedStress = isNaN(maxStress) || maxStress === 0 ? 0 : stress / maxStress;
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
  const [prompt, setPrompt] = useState('a long l-bracket');
  const [modelData, setModelData] = useState(null);
  const [session, setSession] = useState(null);

  // Load the ONNX model
  useEffect(() => {
    async function loadModel() {
      try {
        const newSession = await InferenceSession.create('/gnn_surrogate_model.onnx');
        setSession(newSession);
        console.log('ONNX model loaded successfully.');
      } catch (error) {
        console.error('Error loading ONNX model:', error);
      }
    }
    loadModel();
  }, []);

  const generateAndAnalyzeModel = async () => {
    if (!session) {
      console.error("Session not loaded yet");
      return;
    }

    let geometry;
    if (prompt.includes('l-bracket')) {
        let length = 10, width = 2, height = 10, thickness = 2;
        const shape = new THREE.Shape();
        shape.moveTo(0, 0);
        shape.lineTo(length, 0);
        shape.lineTo(length, thickness);
        shape.lineTo(thickness, thickness);
        shape.lineTo(thickness, height);
        shape.lineTo(0, height);
        shape.lineTo(0, 0);
        const extrudeSettings = { depth: width, bevelEnabled: false };
        geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);

    } else { // Default to beam
        let length = 10, width = 2, height = 2; // Defaults
        if (prompt.includes('long')) length = 20;
        if (prompt.includes('short')) length = 5;
        if (prompt.includes('wide')) width = 4;
        if (prompt.includes('narrow')) width = 1;
        if (prompt.includes('tall')) height = 4;
        if (prompt.includes('flat')) height = 1;
        geometry = new THREE.BoxGeometry(length, width, height, 10, 10, 10);
    }

    const vertices = geometry.attributes.position.array;
    const edges = [];
    if (geometry.index) {
      const indices = geometry.index.array;
      for (let i = 0; i < indices.length; i += 3) {
        edges.push([indices[i], indices[i+1]]);
        edges.push([indices[i+1], indices[i+2]]);
        edges.push([indices[i+2], indices[i]]);
      }
    } else {
      // Handle non-indexed geometry
      for (let i = 0; i < vertices.length / 9; i++) {
        const i3 = i * 3;
        edges.push([i3, i3 + 1]);
        edges.push([i3 + 1, i3 + 2]);
        edges.push([i3 + 2, i3]);
      }
    }

    const x = new Tensor('float32', vertices, [vertices.length / 3, 3]);
    const edge_index_data = new Int32Array(edges.flat());
    const edge_index = new Tensor('int32', edge_index_data, [2, edges.length]);

    const feeds = { x: x, edge_index: edge_index };
    const results = await session.run(feeds);
    const stress = results.output.data;

    setModelData({ geometry, stressData: Array.from(stress) });
  };

  return (
    <div className="App">
      <div className="controls">
        <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        <button onClick={generateAndAnalyzeModel} disabled={!session}>
          {session ? 'Generate and Analyze' : 'Loading Model...'}
        </button>
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
