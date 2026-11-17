import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_community.vectorstores import SupabaseVectorStore
from app.embeddings import get_embeddings_model

load_dotenv()

def get_supabase_client() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in your .env file.")
        
    return create_client(supabase_url, supabase_key)

def get_vector_store() -> SupabaseVectorStore:
    """
    Returns the LangChain SupabaseVectorStore targeting the isolated 'fin_' tables.
    """
    client = get_supabase_client()
    embeddings = get_embeddings_model()
    
    vector_store = SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name="fin_documents",
        query_name="fin_match_documents"
    )
    return vector_store

def store_chunks(chunks) -> None:
    """
    Stores document chunks and embeddings into fin_documents.
    """
    vector_store = get_vector_store()
    print(f"Storing {len(chunks)} chunks into Supabase (fin_documents)...")
    vector_store.add_documents(chunks)
    print("Successfully stored chunks in Supabase pgvector.")

if __name__ == "__main__":
    try:
        client = get_supabase_client()
        print("Successfully connected to Supabase client.")
    except Exception as e:
        print(f"Supabase connection error: {e}")