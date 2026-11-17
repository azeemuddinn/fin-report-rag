import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.retrieval import retrieve_relevant_chunks

load_dotenv()

def get_rag_chain():
    """
    Initializes the Gemini LLM and builds the RAG prompt chain.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    # Initialize Gemini chat model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.1
    )

    

    # Define prompt template enforcing grounding and source citations
    template = """You are an expert financial analyst assistant. Answer the user's question accurately using ONLY the provided context from the financial report.
If the answer cannot be found within the provided context, explicitly state that the information is absent from the document. Do not invent or fabricate any answers.
Always cite the source page numbers referenced in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = ChatPromptTemplate.from_template(template)
    
    # Chain components together
    chain = prompt | llm | StrOutputParser()
    return chain

def answer_question(query: str, k: int = 4) -> dict:
    """
    Executes the full RAG pipeline: retrieval -> context assembly -> Gemini answer generation.
    Returns the generated answer and the source references.
    """
    # 1. Retrieve relevant chunks
    docs_with_scores = retrieve_relevant_chunks(query, k=k)
    
    if not docs_with_scores:
        return {
            "answer": "No relevant information found in the document.",
            "sources": []
        }

    # 2. Format context and collect unique sources
    context_texts = []
    sources = set()
    
    for doc, score in docs_with_scores:
        page_num = doc.metadata.get("page", "Unknown")
        source_file = os.path.basename(doc.metadata.get("source", "Report"))
        context_texts.append(f"[Source: {source_file}, Page {page_num}]\n{doc.page_content}")
        sources.add(f"{source_file} (Page {page_num})")

    combined_context = "\n\n---\n\n".join(context_texts)

    # 3. Generate answer using Gemini chain
    chain = get_rag_chain()
    print("Generating answer from Gemini...")
    answer = chain.invoke({"context": combined_context, "question": query})

    return {
        "answer": answer,
        "sources": list(sources)
    }

if __name__ == "__main__":
    # Quick test snippet
    test_query = "What were the total revenues reported?"
    try:
        result = answer_question(test_query)
        print("\n--- Answer ---")
        print(result["answer"])
        print("\n--- Sources ---")
        print(result["sources"])
    except Exception as e:
        print(f"RAG chain test error: {e}")