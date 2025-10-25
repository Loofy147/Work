import numpy as np
import trimesh
from Pynite import FEModel3D
import os

import shutil

# --- Configuration ---
DATASET_DIR = "ml/dataset"
NUM_SAMPLES = 10
MIN_LENGTH = 10
MAX_LENGTH = 100
MIN_WIDTH = 5
MAX_WIDTH = 20
MIN_HEIGHT = 5
MAX_HEIGHT = 20

# --- Material Properties (Steel) ---
E = 200 * 10**9  # Modulus of Elasticity (Pa)
G = 75 * 10**9   # Shear Modulus (Pa)
nu = 0.3         # Poisson's Ratio
rho = 7850       # Density (kg/m^3)

def create_beam_mesh(length, width, height):
    """Creates a simple beam mesh using trimesh."""
    mesh = trimesh.creation.box(extents=[length, width, height])
    return mesh

def analyze_beam(length, width, height):
    """Analyzes a simple beam using PyNiteFEA."""
    # Create a new finite element model
    beam_model = FEModel3D()

    # Add nodes
    beam_model.add_node("N1", 0, 0, 0)
    beam_model.add_node("N2", length, 0, 0)

    # Define a rectangular section
    J = (width * height**3) / 12
    Iy = (height * width**3) / 12
    Iz = (width * height**3) / 12
    A = width * height

    # Add a material
    beam_model.add_material("Steel", E, G, nu, rho)

    # Define a rectangular section
    J = (width * height**3) / 12
    Iy = (height * width**3) / 12
    Iz = (width * height**3) / 12
    A = width * height
    beam_model.add_section("Rect", A, Iy, Iz, J)

    # Add a member between the two nodes
    beam_model.add_member("M1", "N1", "N2", "Steel", "Rect")

    # Add supports
    beam_model.def_support("N1", True, True, True, True, True, True)

    # Add a point load at the free end
    beam_model.add_node_load("N2", "FZ", -1000, case="Live") # 1000 N downward force

    # Add a load combination
    beam_model.add_load_combo("Combo1", {"Live": 1.0})

    # Analyze the model
    beam_model.analyze(check_stability=False)

    # Get the maximum stress
    # Note: PyniteFEA's stress outputs are complex; we'll simplify for the MVP
    # and just use the maximum moment to approximate stress.
    # A real implementation would require more detailed stress calculations.
    moment_y = beam_model.members["M1"].moment_array("My", 10, "Combo1")
    moment_z = beam_model.members["M1"].moment_array("Mz", 10, "Combo1")
    max_moment = max(np.max(np.abs(moment_y)), np.max(np.abs(moment_z)))

    return max_moment

def generate_dataset():
    """Generates a dataset of beams and their analysis results."""
    os.makedirs(DATASET_DIR, exist_ok=True)

    for i in range(NUM_SAMPLES):
        print(f"Generating sample {i+1}/{NUM_SAMPLES}...")

        # Generate random dimensions
        length = np.random.uniform(MIN_LENGTH, MAX_LENGTH)
        width = np.random.uniform(MIN_WIDTH, MAX_WIDTH)
        height = np.random.uniform(MIN_HEIGHT, MAX_HEIGHT)

        # Create the mesh
        mesh = create_beam_mesh(length, width, height)
        mesh_path = os.path.join(DATASET_DIR, f"beam_{i}.ply")
        mesh.export(mesh_path)

        # Analyze the beam
        max_moment = analyze_beam(length, width, height)

        # Save the analysis result
        result_path = os.path.join(DATASET_DIR, f"beam_{i}.txt")
        with open(result_path, "w") as f:
            f.write(str(max_moment))

    print("Dataset generation complete.")

if __name__ == "__main__":
    generate_dataset()
