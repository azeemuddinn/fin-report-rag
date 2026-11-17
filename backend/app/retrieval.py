from typing import List, Tuple
from langchain_core.documents import Document
from app.vector_store import get_supabase_client
from app.embeddings import get_embeddings_model

def retrieve_relevant_chunks(query: str, k: int = 4) -> List[Tuple[Document, float]]:
    """
    Performs a direct similarity search using the Supabase RPC function 'fin_match_documents'.
    Returns a list of tuples containing (Document, similarity_score).
    """
    client = get_supabase_client()
    embeddings_model = get_embeddings_model()
    
    print(f"Retrieving top {k} relevant chunks for query: '{query}'...")
    
    # 1. Embed the query string
    query_embedding = embeddings_model.embed_query(query)
    
    # 2. Call the custom Supabase RPC function
    response = client.rpc(
        "fin_match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": k
        }
    ).execute()
    
    data = response.data
    results = []
    
    for row in data:
        doc = Document(
            page_content=row.get("content", ""),
            metadata=row.get("metadata", {})
        )
        score = row.get("similarity", 0.0)
        results.append((doc, score))
        
    print(f"Successfully retrieved {len(results)} chunks via RPC.")
    return results

if __name__ == "__main__":
    test_query = "What is the financial summary?"
    try:
        docs_and_scores = retrieve_relevant_chunks(test_query)
        for doc, score in docs_and_scores:
            print(f"- [Score: {score:.4f}] Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:150]}...")
    except Exception as e:
        print(f"Retrieval test error: {e}")