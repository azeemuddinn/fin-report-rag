import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """
    Initializes and returns the Google Gemini embeddings model (gemini-embedding-001).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing. Check your .env file.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
        output_dimensionality=768
    )
    return embeddings

if __name__ == "__main__":
    try:
        model = get_embeddings_model()
        test_vector = model.embed_query("Test embedding generation for financial report.")
        print(f"Successfully generated embedding vector of dimension: {len(test_vector)}")
    except Exception as e:
        print(f"Error testing embeddings: {e}")