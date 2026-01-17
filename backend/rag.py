import os
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding_utils import embed_texts
from faiss_utils import build_index, retrieve_chunks

class RAGService:
    def __init__(self):
        # Resolve path relative to this file (backend/rag.py) -> backend/data
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, "data")
        self.index_name = "faiss_index"
        
    def chunk_text(self, text):
        """
        Chunks text.
        Size: 1000 chars (approx) since we are moving away from tiktoken strictness
        Overlap: 200 chars
        """
        # Simple character splitter is safer if we drop tiktoken, 
        # but tiktoken is installed and good. Let's keep using it or switch to standard.
        # User said "Use Gemini", implies removing OpenAI deps.
        # Let's use standard recursive splitter to be vendor neutral.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""] 
        )
        return text_splitter.split_text(text)

    def ingest_pdf(self, filename="Insurance_FAQ.pdf"):
        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            return {"error": f"File not found at {file_path}"}
            
        # 1. Read PDF
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            return {"error": f"Failed to read PDF: {str(e)}"}
            
        # 2. Chunking
        chunks = self.chunk_text(text)
        if not chunks:
             return {"message": "No text extracted from PDF"}

        # 3. Embedding
        try:
            vectors = embed_texts(chunks)
        except Exception as e:
            return {"error": f"Embedding failed: {str(e)}"}

        # 4. Indexing
        try:
            build_index(chunks, vectors, index_name=self.index_name, data_dir=self.data_dir)
        except Exception as e:
            return {"error": f"Indexing failed: {str(e)}"}
            
        return {"status": "success", "chunks_created": len(chunks)}

    def answer_question(self, question):
        # 1. Retrieve
        try:
            # Need to embed query with task_type="retrieval_query" ideally, 
            # but our util uses "retrieval_document". 
            # For simplicity in this util, we reused the function.
            # In a prod system, we'd add a parameter to embed_texts.
            chunks = retrieve_chunks(question, index_name=self.index_name, data_dir=self.data_dir)
        except Exception as e:
            return "System is not ready. Please ingest a PDF first."

        if not chunks:
            return "I couldn't find any relevant information in the documents."
            
        context = "\n\n".join(chunks)
        
        # 2. Generate Answer with Gemini
        import google.generativeai as genai
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "GEMINI_API_KEY not set."
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""You are a helpful assistant. Answer the question based only on the following context. If the answer is not in the context, say so.

Context:
{context}

Question: {question}
"""
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"

rag_service = RAGService()
