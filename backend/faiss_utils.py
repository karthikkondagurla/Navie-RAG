import faiss
import numpy as np
import pickle
import os
from embedding_utils import embed_texts

def build_index(chunks: list[str], embeddings: np.ndarray, index_name: str = "faiss_index", data_dir: str = "data"):
    """
    Builds a FAISS index from embeddings and saves it along with the text chunks.
    
    Args:
        chunks: List of text strings corresponding to embeddings.
        embeddings: Numpy array of floats (shape NxD).
        index_name: Base name for the index files.
        data_dir: Directory to save files in.
        
    Returns:
        tuple: (index_path, chunks_path)
    """
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)
        
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Save Index
    index_path = os.path.join(data_dir, f"{index_name}.index")
    faiss.write_index(index, index_path)
    
    # Save Chunks (metadata)
    chunks_path = os.path.join(data_dir, f"{index_name}.pkl")
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)
        
    print(f"Index built with {index.ntotal} vectors.")
    return index_path, chunks_path

def retrieve_chunks(query: str, index_name: str = "faiss_index", data_dir: str = "data", top_k: int = 3):
    """
    Embeds the query, searches the FAISS index, and returns top-k relevant chunks.
    
    Args:
        query: User question string.
        index_name: Name of index to load.
        data_dir: Directory where index is stored.
        top_k: Number of chunks to return.
        
    Returns:
        list[str]: list of matching text chunks.
    """
    # Load Index
    index_path = os.path.join(data_dir, f"{index_name}.index")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index not found at {index_path}")
        
    index = faiss.read_index(index_path)
    
    # Load Chunks
    chunks_path = os.path.join(data_dir, f"{index_name}.pkl")
    if not os.path.exists(chunks_path):
        raise FileNotFoundError(f"Chunks not found at {chunks_path}")
        
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    
    # Embed Query
    # embed_texts returns shape (N, D), we need (1, D) for search
    query_vectors = embed_texts([query]) 
    
    # Search
    distances, indices = index.search(query_vectors, top_k)
    
    # Retrieve Results
    results = []
    # indices is shape (1, k)
    for idx in indices[0]:
        if idx != -1 and idx < len(chunks):
            results.append(chunks[idx])
            
    return results
