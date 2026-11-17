# Fin-Report-RAG

An enterprise-grade, stateful **Retrieval-Augmented Generation (RAG)** system built with **LangGraph, FastAPI, Supabase (pgvector), Google Gemini, and Groq**.

This application automates financial document analysis using **Corrective RAG (CRAG)**, featuring automated document relevance grading, multi-LLM fallback resilience, and native LangSmith telemetry tracing.

## Architecture & Core Features

1. **Stateful Graph Orchestration (LangGraph)**  
   Moves beyond linear pipelines into a controlled graph state machine:

   `retrieve` → `grade_documents` → `generate`

2. **Corrective Document Grading**  
   Automatically evaluates retrieved chunks for relevance to eliminate retrieval noise before LLM generation.

3. **Resilient Multi-LLM Fallback Stack**  
   Uses Google Gemini 2.5 Flash as the primary model, with automated runtime failover to Groq (`openai/gpt-oss-120b`) through LangChain's `.with_fallbacks()`.

4. **Production Observability**  
   Integrated with LangSmith for end-to-end trace auditing, latency tracking, and child-run execution inspection.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend & Orchestration | Python, FastAPI, LangGraph, LangChain (LCEL) |
| Vector Database | Supabase PostgreSQL, pgvector |
| Primary LLM | Google Gemini API (`gemini-2.5-flash`) |
| Fallback LLM | Groq LPU (`openai/gpt-oss-120b`) |
| Telemetry | LangSmith |

## Project Structure

```text
fin-report-rag/
├── backend/
│   ├── app/                  # Ingestion, chunking, retrieval, vector store modules
│   ├── main.py               # FastAPI application entrypoint
│   └── rag_graph.py          # LangGraph CRAG state machine definition
├── frontend/                 # Next.js 15 App Router application
└── .gitignore                # Git ignore rules
```

## Getting Started

### Prerequisites

Make sure you have the following installed or configured:

- Python 3.10+
- Node.js 18+
- A Supabase project with pgvector enabled
- Google Gemini API key
- Groq API key
- LangSmith API key

### 1. Backend Setup (FastAPI)

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key

# LangSmith Telemetry Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=fin-report-rag
```

#### Start the Backend

```bash
uvicorn main:app --reload
```

The backend will be available at:

- **API:** http://127.0.0.1:8000
- **Swagger documentation:** http://127.0.0.1:8000/docs

### 2. Frontend Setup (Next.js)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the application in your browser:

http://localhost:3000

## Environment Variables Reference

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |
| `GEMINI_API_KEY` | Google Gemini API key (Primary LLM) |
| `GROQ_API_KEY` | Groq API key (Fallback LLM) |
| `LANGSMITH_TRACING` | Set to `true` to enable tracing |
| `LANGSMITH_API_KEY` | LangSmith telemetry API key |
| `LANGSMITH_PROJECT` | LangSmith project name |

## Security

- Keep all `.env` configuration restricted to the backend.
- Never expose Supabase service role keys or LLM API credentials in client-side code.
- Never commit API keys or environment files to version control.
- Ensure `.env` is included in `.gitignore`.

## Project Status

**Features:** LangGraph orchestration, Corrective RAG, multi-LLM fallback, and LangSmith tracing.

**Environment:** Development setup documented.