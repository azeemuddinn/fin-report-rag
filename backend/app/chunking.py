from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(
    documents: List[Document], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Splits LangChain Documents into smaller chunks while preserving metadata (like page numbers).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks (size: {chunk_size}, overlap: {chunk_overlap}).")
    return chunks

if __name__ == "__main__":
    from app.ingestion import load_pdf
    import os
    sample_pdf = os.path.join("documents", "sample_report.pdf")
    if os.path.exists(sample_pdf):
        docs = load_pdf(sample_pdf)
        chunks = chunk_documents(docs)
        print(f"Sample chunk 1 metadata: {chunks[0].metadata}")