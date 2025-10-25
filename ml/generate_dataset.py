import numpy as np
import trimesh
import os

# --- Configuration ---
DATASET_DIR = "ml/dataset_v2"
NUM_SAMPLES = 50  # Increased sample size for better training
MIN_LENGTH = 10
MAX_LENGTH = 100
MIN_WIDTH = 5
MAX_WIDTH = 20
MIN_HEIGHT = 5
MAX_HEIGHT = 20

def pseudo_analyze_beam(mesh):
    """
    Performs a pseudo-simulation to generate a stress-like distribution.
    Stress is calculated as the squared distance from the fixed end (x=0).
    """
    vertices = mesh.vertices
    # Calculate stress as the squared distance from the x=0 plane
    stress = vertices[:, 0]**2
    return stress

def generate_dataset():
    """Generates the dataset with pseudo-simulation results."""
    if os.path.exists(DATASET_DIR):
        # Clear old dataset if it exists
        for file in os.listdir(DATASET_DIR):
            os.remove(os.path.join(DATASET_DIR, file))
    else:
        os.makedirs(DATASET_DIR)

    for i in range(NUM_SAMPLES):
        print(f"Generating sample {i+1}/{NUM_SAMPLES}...")

        # Generate random dimensions
        length = np.random.uniform(MIN_LENGTH, MAX_LENGTH)
        width = np.random.uniform(MIN_WIDTH, MAX_WIDTH)
        height = np.random.uniform(MIN_HEIGHT, MAX_HEIGHT)

        # Create the mesh
        mesh = trimesh.creation.box(extents=[length, width, height])

        # Perform pseudo-analysis
        stress = pseudo_analyze_beam(mesh)

        # Save the mesh and stress results
        mesh_path = os.path.join(DATASET_DIR, f"beam_{i}.ply")
        mesh.export(mesh_path)

        result_path = os.path.join(DATASET_DIR, f"beam_{i}_stress.txt")
        np.savetxt(result_path, stress)

    print("Dataset generation complete.")

if __name__ == "__main__":
    generate_dataset()
