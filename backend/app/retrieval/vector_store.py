# import faiss
# import json
# import numpy as np
# from pathlib import Path


# class VectorStore:
#     def __init__(self, dim: int, index_path: str):
#         self.dim = dim
#         self.index_path = Path(index_path)
#         self.index = faiss.IndexFlatIP(dim)
#         self.metadata = []

#     def add(self, embeddings: np.ndarray, metadata: list):
#         assert len(embeddings) == len(metadata)
#         self.index.add(embeddings)
#         self.metadata.extend(metadata)

#     def save(self):
#         self.index_path.parent.mkdir(parents=True, exist_ok=True)
#         faiss.write_index(self.index, str(self.index_path))
#         with open(self.index_path.with_suffix(".meta.json"), "w") as f:
#             json.dump(self.metadata, f, indent=2)

#     def load(self):
#         self.index = faiss.read_index(str(self.index_path))
#         with open(self.index_path.with_suffix(".meta.json")) as f:
#             self.metadata = json.load(f)

#     def search(self, query_embedding: np.ndarray, k: int = 5):
#         scores, indices = self.index.search(
#             query_embedding.reshape(1, -1), k
#         )

#         results = []
#         for score, idx in zip(scores[0], indices[0]):
#             if idx == -1:
#                 continue
#             results.append({
#                 "score": float(score),
#                 **self.metadata[idx]
#             })

#         return results


import faiss
import numpy as np
import pickle
import os
from typing import List, Dict

class VectorStore:
    def __init__(self, dimension: int, index_dir: str = "data/indices/paper1"):
        self.dimension = dimension
        self.index_dir = index_dir
        self.index_path = os.path.join(index_dir, "index.faiss")
        self.meta_path = os.path.join(index_dir, "metadata.pkl")
        
        # Initialize Index (L2 = Euclidean Distance)
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata: List[Dict] = []

    def add(self, embeddings: np.ndarray, documents: List[Dict]):
        if len(documents) != embeddings.shape[0]:
            raise ValueError("Count mismatch between embeddings and documents")
        
        self.index.add(embeddings)
        self.metadata.extend(documents)

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict]:
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                res = self.metadata[idx].copy()
                res["score"] = float(distances[0][i])
                results.append(res)
        return results

    def save(self):
        os.makedirs(self.index_dir, exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"✅ Index saved to {self.index_dir}")

    def load(self):
        if not os.path.exists(self.index_path):
            print("⚠️ No index found. Starting fresh.")
            return

        self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        print(f"📂 Loaded index with {self.index.ntotal} vectors.")