import os
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion import load_pdf
from app.chunking import chunk_documents
from app.vector_store import store_chunks
from app.rag_chain import llm                  # Import your resilient LLM from rag_chain
from app.retrieval import get_rag_retriever    # Import the retriever factory function
from app.rag_graph import create_rag_graph     # Import your LangGraph workflow builder
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FinReport RAG API", 
    description="API for ingesting financial PDF reports and querying them using LangGraph CRAG, Gemini, and Supabase pgvector.",
    version="2.0"
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

# Initialize the retriever and LangGraph Corrective RAG workflow on startup
retriever = get_rag_retriever(k=4)
rag_graph = create_rag_graph(retriever, llm)

class QueryRequest(BaseModel):
    question: str
    k: int = 4

@app.get("/")
def read_root():
    return {"message": "Welcome to FinReport RAG API (LangGraph Enabled). Navigate to /docs for interactive Swagger UI."}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(DOCUMENTS_DIR, file.filename)
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
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
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # Invoke the LangGraph state graph
        state_input = {"question": request.question, "documents": [], "generation": "", "web_search_needed": "no"}
        result = rag_graph.invoke(state_input)
        
        # Extract unique source metadata from validated chunks
        sources = []
        for doc in result.get("documents", []):
            source_file = doc.metadata.get("source", "unknown_file")
            page_num = doc.metadata.get("page", doc.metadata.get("page_number", "N/A"))
            page_label = f"Page {page_num + 1}" if isinstance(page_num, int) else f"Page {page_num}"
            sources.append(f"{source_file} ({page_label})")
        sources = list(dict.fromkeys(sources))

        return {
            "question": request.question,
            "answer": result.get("generation", "No generation produced."),
            "sources": sources
        }
    except Exception as e:
        print("--- RAG GRAPH ERROR TRACEBACK ---")
        traceback.print_exc()
        print("---------------------------------")
        raise HTTPException(status_code=500, detail=f"LangGraph execution error: {str(e)}")