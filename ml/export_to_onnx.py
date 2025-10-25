import torch
from torch_geometric.data import Data
from train_surrogate import GNN  # Import the GNN model class
import os

# --- Configuration ---
MODEL_PATH = "ml/gnn_surrogate_model.pt"
ONNX_MODEL_PATH = "ml/gnn_surrogate_model.onnx"

def main():
    """Loads the trained GNN model and exports it to ONNX format."""
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    # Load the trained model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = GNN().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    print("GNN model loaded successfully.")

    # Create dummy input for the ONNX export
    dummy_x = torch.randn(10, 3).to(device)  # 10 vertices, 3 features (x, y, z)
    dummy_edge_index = torch.randint(0, 10, (2, 20)).to(device) # 20 edges

    # Export the model
    print(f"Exporting model to {ONNX_MODEL_PATH}...")
    torch.onnx.export(model,
                      (dummy_x, dummy_edge_index),
                      ONNX_MODEL_PATH,
                      export_params=True,
                      opset_version=18,
                      do_constant_folding=True,
                      input_names=['x', 'edge_index'],
                      output_names=['output'],
                      dynamic_axes={'x': {0: 'num_nodes'},
                                    'edge_index': {1: 'num_edges'},
                                    'output': {0: 'num_nodes'}})

    print("Model exported to ONNX successfully.")

if __name__ == "__main__":
    main()
