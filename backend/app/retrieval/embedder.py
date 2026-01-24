
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # "all-MiniLM-L6-v2" is fast and good for generic retrieval
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of texts."""
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query string."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.reshape(1, -1)
