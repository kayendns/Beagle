from .database_manager import DatabaseManager
import torch.nn.functional as F

class SearchEngine:
    def __init__(self, database_manager:DatabaseManager, similarity_metric: str = "cos"):
        self.database_manager = database_manager
        self.similarity_metric = similarity_metric

    # This loads all embeddings from the database into memory. Computationally problematic for large databases.
    def search_for(self, query):
        results = []
        rows = self.database_manager.fetch_all_embeddings() # Assuming this returns a list of (file_path, tensor)
        for file_path, embedding in rows:
            similarity = self.measure_similarity(query, embedding)
            results.append((file_path, similarity))
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        return sorted_results

    def measure_similarity(self, t1, t2):
        # Make sure the tensors are on the same device.
        if t1.device != t2.device:
            raise Exception("Tensors are on different devices")

        if self.similarity_metric == "cos":
            return F.cosine_similarity(t1, t2, dim=1)
        else:
            raise Exception("Unsupported similarity measure")
