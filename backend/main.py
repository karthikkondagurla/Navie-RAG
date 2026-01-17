from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Optional dotenv loading (rag.py also loads it)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="RAG 2.0 Backend")

# CORS setup
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "RAG 2.0 Backend API"}

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@app.post("/ingest")
def ingest_data():
    from rag import rag_service
    return rag_service.ingest_pdf()

@app.post("/chat")
def chat(request: ChatRequest):
    from rag import rag_service
    response = rag_service.answer_question(request.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    # Reload needs string import, works better with app instance directly in code if running simple
    uvicorn.run(app, host="0.0.0.0", port=8000)
