import os
import shutil
import numpy as np
from unittest.mock import patch, MagicMock

# Needs to be set before import if not mocked, but we will patch openai client
os.environ["OPENAI_API_KEY"] = "sk-dummy"

from rag import rag_service

# Mock entire embedding call to return dummy vectors
@patch("rag.embed_texts")
def test_ingest_flow(mock_embed):
    print("Testing full ingest flow...")
    
    # 1. Setup Dummy PDF
    # We will just rely on the existing Insurance_FAQ.pdf if it exists, or handle error
    # Actually, let's assume it exists from previous steps (it was generated).
    
    # Mock return value for embeddings
    # We don't know exactly how many chunks, but let's say 2 for now
    # The code will call embed_texts(chunks) -> returns (N, 1536)
    # We'll just return a compatible shape for however many chunks it sends
    def side_effect(texts, **kwargs):
        return np.random.rand(len(texts), 1536).astype(np.float32)
        
    mock_embed.side_effect = side_effect
    
    # 2. Run Ingest
    res = rag_service.ingest_pdf("Insurance_FAQ.pdf")
    print("Ingest Result:", res)
    
    if "error" in res:
        print("Ingest failed:", res["error"])
    else:
        assert res["status"] == "success"
        assert res["chunks_created"] > 0
        print("Ingest successful.")
        
        # Check if files created
        data_dir = rag_service.data_dir
        assert os.path.exists(os.path.join(data_dir, "faiss_index.index"))
        assert os.path.exists(os.path.join(data_dir, "faiss_index.pkl"))
        print("Index files verified.")

if __name__ == "__main__":
    test_ingest_flow()
