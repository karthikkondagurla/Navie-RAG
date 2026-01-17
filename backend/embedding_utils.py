import os
import numpy as np
import google.generativeai as genai
from typing import List

def embed_texts(texts: List[str], model="models/text-embedding-004", batch_size=100) -> np.ndarray:
    """
    Embeds a list of texts using Google Gemini embedding model.
    Handles batching efficiently and returns numpy float32 arrays.
    
    Args:
        texts: List of strings to embed.
        model: Gemini model identifier.
        batch_size: Number of texts to send in one API call.
        
    Returns:
        np.ndarray: A 2D numpy array of shape (N, D) with dtype float32.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
        
    genai.configure(api_key=api_key)
    
    # Pre-clean texts: Gemini prefers no newlines in some embedding models, 
    # but modern text-embedding-004 is robust. removing newlines is still safe practice.
    texts = [str(t).replace("\n", " ") for t in texts]
    
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        try:
            # Gemini embedding API structure
            result = genai.embed_content(
                model=model,
                content=batch,
                task_type="retrieval_document", # Optimize for storage/retrieval
                title=None
            )
            # result['embedding'] is a list of lists if batch
            if 'embedding' in result:
                batch_embeddings = result['embedding']
                all_embeddings.extend(batch_embeddings)
            else:
                # Handle potential single return or error structure
                 raise ValueError("No embeddings returned")
                 
        except Exception as e:
            print(f"Error embedding batch {i}-{i+batch_size}: {e}")
            raise e

    # Convert to numpy float32
    return np.array(all_embeddings, dtype=np.float32)
