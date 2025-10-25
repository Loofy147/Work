from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# --- Model Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'surrogate_model.joblib')
model = None

def load_model():
    """Loads the trained surrogate model."""
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Error: Model not found at {MODEL_PATH}")

@app.route('/predict', methods=['POST'])
def predict():
    """Makes a prediction using the loaded model."""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    if 'features' not in data:
        return jsonify({"error": "Missing 'features' in request"}), 400

    try:
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model()
    app.run(port=5000)
