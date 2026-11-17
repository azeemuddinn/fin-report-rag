# Fin-Report-RAG

A modular **Retrieval-Augmented Generation (RAG)** application that enables users to query quarterly financial reports in PDF format and retrieve context-aware answers using an LLM.

Built with **Next.js 15, FastAPI, Supabase (pgvector), and Google Gemini API**, the project demonstrates how to build an end-to-end RAG pipeline for financial document analysis.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | Python, FastAPI |
| Vector Database | Supabase PostgreSQL, pgvector |
| LLM | Google Gemini API |
| Architecture | Retrieval-Augmented Generation (RAG) |

## Project Structure

```text
fin-report-rag/
├── backend/          # FastAPI backend and RAG pipeline
├── frontend/         # Next.js 15 App Router application
└── .gitignore        # Git ignore rules
```

## Getting Started

Follow these steps to run the application locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Node.js 18+
- npm
- A Supabase project with pgvector enabled
- Google Gemini API key

### 1. Backend Setup (FastAPI)

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

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

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
GEMINI_API_KEY=your_gemini_api_key
```

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The backend will be available at:

http://127.0.0.1:8000

### 2. Frontend Setup (Next.js)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Next.js development server:

```bash
npm run dev
```

Open the application in your browser:

http://localhost:3000

## Environment Variables

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |
| `GEMINI_API_KEY` | Google Gemini API key |

**Security Note:** Never commit your `.env` files or expose your Supabase service role key in frontend code. Keep sensitive credentials restricted to the backend.

## Project Goal

The goal of this project is to explore and implement a practical RAG architecture for financial document analysis, connecting document ingestion, vector-based retrieval, and LLM-powered response generation.

---

**Status:** Under Development