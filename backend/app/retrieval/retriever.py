

from retrieval.embedder import Embedder
from retrieval.vector_store import VectorStore

class Retriever:
    def __init__(self, index_dir: str = "data/indices/paper1"):
        self.embedder = Embedder()
        self.store = VectorStore(dimension=self.embedder.dimension, index_dir=index_dir)
        self.store.load()

    def retrieve(self, query: str, k: int = 5):
        query_vec = self.embedder.embed_query(query)
        results = self.store.search(query_vec, k=k)
        return results
