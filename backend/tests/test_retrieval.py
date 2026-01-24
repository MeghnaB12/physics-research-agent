import pytest
import shutil
import os
import numpy as np
from retrieval.embedder import Embedder
from retrieval.vector_store import VectorStore

TEST_INDEX_DIR = "data/test_indices"

@pytest.fixture
def setup_teardown():
    # Setup
    os.makedirs(TEST_INDEX_DIR, exist_ok=True)
    yield
    # Teardown
    if os.path.exists(TEST_INDEX_DIR):
        shutil.rmtree(TEST_INDEX_DIR)

def test_embedder_output():
    emb = Embedder()
    vec = emb.embed_query("Hello world")
    assert vec.shape == (1, 384)

def test_store_save_load_search(setup_teardown):
    dim = 384
    store = VectorStore(dimension=dim, index_dir=TEST_INDEX_DIR)
  
    vecs = np.random.rand(2, dim).astype('float32')
    docs = [{"id": 1, "text": "A"}, {"id": 2, "text": "B"}]
    
    store.add(vecs, docs)
    store.save()
    
    # Load new instance
    new_store = VectorStore(dimension=dim, index_dir=TEST_INDEX_DIR)
    new_store.load()
    
    assert new_store.index.ntotal == 2
    
    # Search
    results = new_store.search(vecs[0:1], k=1)
    assert len(results) == 1
    assert results[0]["text"] == "A"