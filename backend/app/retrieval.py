from typing import List, Tuple
from langchain_core.documents import Document
from app.vector_store import get_vector_store

def get_rag_retriever(k: int = 4):
    """
    Returns a LangChain-native retriever interface configured with k.
    """
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

def retrieve_relevant_chunks(query: str, k: int = 4) -> List[Tuple[Document, float]]:
    """
    Performs retrieval using the LangChain retriever interface.
    (Note: Standard retrievers return Documents without distance scores; 
    we fetch documents and assign a default score of 0.0 or use similarity search).
    """
    vector_store = get_vector_store()
    print(f"Retrieving top {k} relevant chunks for query: '{query}'...")
    
    # Use similarity search with score if supported, or standard retriever docs
    # SupabaseVectorStore supports similarity_search_with_score under the hood via underlying vector store methods
    try:
        results = vector_store.similarity_search_with_score(query, k=k)
    except Exception:
        docs = vector_store.similarity_search(query, k=k)
        results = [(doc, 0.0) for doc in docs]
        
    print(f"Successfully retrieved {len(results)} chunks.")
    return results