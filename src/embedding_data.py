from dataclasses import dataclass
import torch

@dataclass
class EmbeddingData:
    file_path: str
    embedding: torch.Tensor
