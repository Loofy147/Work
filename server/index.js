const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const port = 8000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.post('/generate', async (req, res) => {
  const { text } = req.body;
  console.log(`Received prompt: ${text}`);

  // For the MVP, we'll use fixed dimensions.
  // A real implementation would parse these from the text prompt.
  const features = [50, 10, 10];

  try {
    const response = await axios.post('http://localhost:5000/predict', { features });
    const prediction = response.data.prediction;

    res.json({
      message: 'Model generation started',
      prediction: prediction
    });
  } catch (error) {
    console.error('Error calling predictor service:', error);
    res.status(500).json({ error: 'Error getting prediction' });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
