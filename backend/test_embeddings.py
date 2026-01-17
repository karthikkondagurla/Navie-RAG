import os
import numpy as np
from unittest.mock import MagicMock, patch

from embedding_utils import embed_texts

@patch("embedding_utils.genai")
def test_embeddings(mock_genai):
    texts = ["Hello world", "Another sentence"]
    print(f"Testing Gemini embedding for {len(texts)} texts...")
    
    # Setup mock return
    # embed_content return dict
    mock_genai.embed_content.return_value = {'embedding': [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6]
    ]}
    
    # Call function
    os.environ["GEMINI_API_KEY"] = "dummy-key"
    vectors = embed_texts(texts, batch_size=2)
    
    # Verify configure called
    mock_genai.configure.assert_called_with(api_key="dummy-key")
    
    print("Function returned.")
    print(f"Shape: {vectors.shape}")
    
    assert vectors.shape == (2, 3) 
    assert vectors.dtype == np.float32
    print("Verification successful: returned float32 numpy array.")

if __name__ == "__main__":
    test_embeddings()
