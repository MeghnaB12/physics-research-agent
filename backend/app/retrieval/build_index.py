# import json
# from retrieval.embedder import Embedder
# from retrieval.vector_store import VectorStore

# CHUNKS_PATH = "data/processed/paper1/chunks.json"
# INDEX_PATH = "data/processed/paper1/index.faiss"


# def build_index():
#     with open(CHUNKS_PATH) as f:
#         chunks = json.load(f)

#     texts = [c["text"] for c in chunks]

#     embedder = Embedder()
#     embeddings = embedder.embed_texts(texts)

#     store = VectorStore(dim=embeddings.shape[1], index_path=INDEX_PATH)
#     store.add(
#         embeddings,
#         metadata=chunks
#     )
#     store.save()

#     print(f"✅ Indexed {len(chunks)} chunks")


# if __name__ == "__main__":
#     build_index()


import json
import os
from retrieval.embedder import Embedder
from retrieval.vector_store import VectorStore

# Paths
CHUNKS_PATH = "data/processed/paper1/chunks_enriched.json"
INDEX_DIR = "data/indices/paper1"

def run_indexing():
    if not os.path.exists(CHUNKS_PATH):
        print(f"❌ Error: {CHUNKS_PATH} not found.")
        return

    # 1. Load Data
    print("📂 Loading enriched chunks...")
    with open(CHUNKS_PATH, "r") as f:
        chunks = json.load(f)
    
    texts = [c["text"] for c in chunks]
    
    # 2. Embed
    print(f"🧠 Embedding {len(texts)} chunks...")
    embedder = Embedder()
    vectors = embedder.embed(texts)
    
    # 3. Store
    print("💾 Saving to Vector Store...")
    store = VectorStore(dimension=embedder.dimension, index_dir=INDEX_DIR)
    store.add(vectors, chunks)
    store.save()

if __name__ == "__main__":
    run_indexing()