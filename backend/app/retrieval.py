from typing import List, Tuple
from langchain_core.documents import Document
from app.vector_store import get_vector_store

def retrieve_relevant_chunks(query: str, k: int = 4) -> List[Tuple[Document, float]]:
    """
    Performs a similarity search on Supabase pgvector for the given query.
    Returns a list of tuples containing (Document, similarity_score).
    """
    vector_store = get_vector_store()
    print(f"Retrieving top {k} relevant chunks for query: '{query}'...")
    
    # similarity_search_with_score returns documents and their distance/similarity scores
    results = vector_store.similarity_search_with_score(query, k=k)
    print(f"Successfully retrieved {len(results)} chunks.")
    return results

if __name__ == "__main__":
    # Quick test snippet
    test_query = "What is the financial summary?"
    try:
        docs_and_scores = retrieve_relevant_chunks(test_query)
        for doc, score in docs_and_scores:
            print(f"- [Score: {score:.4f}] Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:150]}...")
    except Exception as e:
        print(f"Retrieval test error: {e}")