import os
import torch
import torch.nn.functional as F
from torch_geometric.data import Dataset, Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv
import trimesh
import numpy as np

# --- Configuration ---
DATASET_DIR = "ml/dataset_v2"
MODEL_PATH = "ml/gnn_surrogate_model.pt"
NUM_EPOCHS = 100
BATCH_SIZE = 10
LEARNING_RATE = 0.01

# 1. Custom Dataset
class BeamDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(BeamDataset, self).__init__(root, transform, pre_transform)

    @property
    def raw_file_names(self):
        return [f for f in os.listdir(self.raw_dir) if f.endswith('.ply')]

    @property
    def processed_file_names(self):
        return [f'data_{i}.pt' for i in range(len(self.raw_file_names))]

    def download(self):
        pass # Data is already in raw_dir

    def process(self):
        idx = 0
        for raw_path in self.raw_paths:
            # Load mesh
            mesh = trimesh.load(raw_path)

            # Node features are the vertex coordinates
            x = torch.tensor(mesh.vertices, dtype=torch.float)

            # Edge index from mesh faces
            edge_index = torch.tensor(mesh.edges.T, dtype=torch.long)

            # Target values (stress)
            stress_path = raw_path.replace('.ply', '_stress.txt')
            y = torch.tensor(np.loadtxt(stress_path), dtype=torch.float).unsqueeze(1)

            data = Data(x=x, edge_index=edge_index, y=y)
            torch.save(data, os.path.join(self.processed_dir, f'data_{idx}.pt'))
            idx += 1

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(os.path.join(self.processed_dir, f'data_{idx}.pt'), weights_only=False)
        return data

# 2. GNN Architecture
class GNN(torch.nn.Module):
    def __init__(self):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(3, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

# 3. Training Loop
def train():
    dataset = BeamDataset(root=DATASET_DIR)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = GNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    model.train()
    for epoch in range(NUM_EPOCHS):
        total_loss = 0
        for data in loader:
            data = data.to(device)
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)
            loss = F.mse_loss(out, data.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * data.num_graphs
        print(f"Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {total_loss / len(loader.dataset)}")

    return model

if __name__ == "__main__":
    print("Training GNN surrogate model...")
    trained_model = train()

    print(f"Saving model to {MODEL_PATH}...")
    torch.save(trained_model.state_dict(), MODEL_PATH)

    print("Model training complete.")
