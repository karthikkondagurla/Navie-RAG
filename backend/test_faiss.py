import numpy as np
import os
import shutil
from unittest.mock import patch, MagicMock

# Mock embedding so we don't need API key for this logic test
with patch("embedding_utils.embed_texts") as mock_embed:
    from faiss_utils import build_index, retrieve_chunks

    def test_faiss_logic():
        # Setup Data
        test_dir = "test_data"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        os.makedirs(test_dir)

        chunks = ["Apple is a fruit", "Car is a vehicle", "Banana is yellow"]
        
        # Mock embeddings: 2 dimensions
        # Apple -> [1, 0]
        # Car -> [0, 1]
        # Banana -> [1, 0] (Similar to Apple)
        fake_embeddings = np.array([
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.1] 
        ], dtype=np.float32)
        
        # 1. Build Index
        print("Building index...")
        build_index(chunks, fake_embeddings, index_name="test", data_dir=test_dir)
        
        # 2. Retrieve
        print("Retrieving...")
        # Query "fruit" -> mock embedding [1, 0]
        mock_embed.return_value = np.array([[1.0, 0.0]], dtype=np.float32)
        
        results = retrieve_chunks("fruit", index_name="test", data_dir=test_dir, top_k=2)
        
        print("Results:", results)
        
        # We expect Apple and Banana to be top 2 because they are close to [1,0]
        assert "Apple is a fruit" in results
        assert "Banana is yellow" in results
        assert "Car is a vehicle" not in results
        
        print("Verification successful!")
        
        # Cleanup
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_faiss_logic()
