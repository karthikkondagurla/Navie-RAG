import os
# Set dummy key before importing rag because it attempts to init OpenAIEmbeddings
os.environ["OPENAI_API_KEY"] = "sk-dummy-key"

from rag import rag_service

def test_chunking():
    # Generate a long string
    # 1 token is roughly 4 chars, so 450 tokens ~ 1800 chars.
    # We want at least 2 chunks.
    long_text = "word " * 600 # 600 words, likely > 450 tokens
    
    try:
        chunks = rag_service.chunk_text(long_text)
        
        print(f"Original text length (words): ~600")
        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i} length (chars): {len(chunk)}")
            
        if len(chunks) > 1:
            print("Chunking successful (multiple chunks created).")
        else:
            print("Warning: Only 1 chunk created, might be expected if tokens < 450.")
    except Exception as e:
        print(f"Chunking failed: {e}")

if __name__ == "__main__":
    test_chunking()
