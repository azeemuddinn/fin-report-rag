import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion import load_pdf
from app.chunking import chunk_documents
from app.vector_store import store_chunks
from app.rag_chain import answer_question
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FinReport RAG API", 
    description="API for ingesting financial PDF reports and querying them using Gemini and Supabase pgvector.",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCUMENTS_DIR = "documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    k: int = 4

@app.get("/")
def read_root():
    return {"message": "Welcome to FinReport RAG API. Navigate to /docs for interactive Swagger UI."}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF report, extracts text, chunks it, and stores embeddings in Supabase.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(DOCUMENTS_DIR, file.filename)
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Execute ingestion pipeline
        docs = load_pdf(file_path)
        chunks = chunk_documents(docs)
        store_chunks(chunks)
        
        return {
            "filename": file.filename,
            "status": "Success",
            "pages_loaded": len(docs),
            "chunks_stored": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.post("/ask/")
def ask_question(request: QueryRequest):
    """
    Asks a question against the ingested financial reports using the RAG chain.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        result = answer_question(request.question, k=request.k)
        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        print("--- RAG ERROR TRACEBACK ---")
        traceback.print_exc()
        print("---------------------------")
        raise HTTPException(status_code=500, detail=f"RAG execution error: {str(e)}")