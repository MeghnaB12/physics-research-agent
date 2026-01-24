# from retrieval.embedder import Embedder
# from retrieval.vector_store import VectorStore
# from retrieval.reranker import Reranker
# from retrieval.adjacency_expander import expand_with_neighbors
# from retrieval.context_packer import ContextPacker


# class Retriever:
#     def __init__(
#         self,
#         index_path: str,
#         embedding_dim: int = 384,
#         top_k: int = 12,
#         max_context_chars: int = 3500
#     ):
#         self.embedder = Embedder()

#         self.store = VectorStore(
#             dim=embedding_dim,
#             index_path=index_path
#         )
#         self.store.load()

#         self.top_k = top_k
#         self.reranker = Reranker()
#         self.context_packer = ContextPacker(max_chars=max_context_chars)

#     # -------------------------
#     # Core retrieval (Week 4.1–4.2)
#     # -------------------------
#     def retrieve(
#         self,
#         query: str,
#         preferred_section: str | None = None
#     ) -> list:
#         """
#         Returns reranked chunks (no stitching).
#         """
#         query_embedding = self.embedder.embed_query(query)

#         initial_results = self.store.search(
#             query_embedding,
#             k=self.top_k
#         )

#         reranked = self.reranker.rerank(
#             initial_results,
#             query=query,
#             preferred_section=preferred_section
#         )

#         return reranked

#     # -------------------------
#     # Answer-ready context (Week 4.3)
#     # -------------------------
#     def retrieve_context(
#         self,
#         query: str,
#         all_chunks: list,
#         preferred_section: str | None = None,
#         neighbor_window: int = 1
#     ) -> str:
#         """
#         Returns LLM-ready stitched context.
#         """

#         ranked = self.retrieve(
#             query=query,
#             preferred_section=preferred_section
#         )

#         expanded = expand_with_neighbors(
#             ranked_chunks=ranked[:6],
#             all_chunks=all_chunks,
#             window=neighbor_window
#         )

#         return self.context_packer.pack(expanded)

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
