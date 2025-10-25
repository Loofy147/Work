import numpy as np
import trimesh
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# --- Configuration ---
DATASET_DIR = "ml/dataset"
MODEL_PATH = "ml/surrogate_model.joblib"

def load_dataset():
    """Loads the dataset from the dataset directory."""
    features = []
    labels = []

    for filename in os.listdir(DATASET_DIR):
        if filename.endswith(".ply"):
            # Load the mesh
            mesh_path = os.path.join(DATASET_DIR, filename)
            mesh = trimesh.load(mesh_path)

            # Extract features (length, width, height)
            length, width, height = mesh.extents
            features.append([length, width, height])

            # Load the corresponding label
            result_path = os.path.join(DATASET_DIR, filename.replace(".ply", ".txt"))
            with open(result_path, "r") as f:
                label = float(f.read())
            labels.append(label)

    return np.array(features), np.array(labels)

def train_model(X, y):
    """Trains a RandomForestRegressor model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model Mean Squared Error: {mse}")

    return model

def main():
    """Loads the dataset, trains the model, and saves it."""
    print("Loading dataset...")
    X, y = load_dataset()

    print("Training model...")
    model = train_model(X, y)

    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)

    print("Model training complete.")

if __name__ == "__main__":
    main()
