import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF file and extracts text page by page into LangChain Documents.
    Includes basic error handling for missing or invalid files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The PDF file at '{file_path}' does not exist.")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"Invalid file format. '{file_path}' must be a PDF document.")

    try:
        print(f"Loading PDF: {file_path}...")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} pages from {file_path}.")
        return documents
    except Exception as e:
        print(f"Error loading PDF {file_path}: {str(e)}")
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

if __name__ == "__main__":
    # Quick test snippet if run directly
    sample_pdf = os.path.join("documents", "sample_report.pdf")
    if os.path.exists(sample_pdf):
        docs = load_pdf(sample_pdf)
        print(f"Sample page 1 metadata: {docs[0].metadata}")
    else:
        print(f"Place a test PDF in the 'documents/' folder to test ingestion.")