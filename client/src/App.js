import React, { useState, Suspense } from 'react';
import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader';
import './App.css';

function Model({ url }) {
  const ply = useLoader(PLYLoader, url);
  return <primitive object={ply} />;
}

function App() {
  const [modelUrl, setModelUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const generateModel = async () => {
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: 'a cube' }),
      });
      const data = await response.json();
      console.log(data.message);
      setPrediction(data.prediction);
      setModelUrl('/cube.ply');
    } catch (error) {
      console.error('Error generating model:', error);
    }
  };

  const logFeedback = (feedback) => {
    console.log(`User feedback: ${feedback}`, {
      prompt: 'a cube', // In a real app, this would be the user's prompt
      prediction: prediction,
      feedback: feedback
    });
  };

  return (
    <div className="App">
      <button onClick={generateModel}>Generate Model</button>
      {prediction && (
        <div className="feedback">
          <h3>Prediction: {prediction}</h3>
          <button onClick={() => logFeedback('good')}>Good Prediction</button>
          <button onClick={() => logFeedback('bad')}>Bad Prediction</button>
        </div>
      )}
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <Suspense fallback={null}>
          {modelUrl && <Model url={modelUrl} />}
        </Suspense>
        <OrbitControls />
      </Canvas>
    </div>
  );
}

export default App;
