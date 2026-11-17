import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.retrieval import get_rag_retriever

load_dotenv()

def get_rag_chain():
    """
    Initializes the Gemini LLM and builds the RAG prompt chain using LCEL.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    llm = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        temperature=0.1
    )

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
    return prompt | llm | StrOutputParser()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(query: str, k: int = 4):
    """
    Executes the 100% LangChain-native RAG pipeline using LCEL primitives.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.1
    )

    retriever = get_rag_retriever(k=k)
    source_docs = retriever.invoke(query)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial analyst assistant. Answer accurately using ONLY the provided context. Cite source pages.\n\nContext:\n{context}"),
        ("human", "{question}")
    ])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print(f"Executing LCEL RAG chain for query: '{query}'...")
    answer = rag_chain.invoke(query)

    sources = []
    for doc in source_docs:
        source_file = doc.metadata.get("source", "unknown_file")
        page_num = doc.metadata.get("page", doc.metadata.get("page_number", "N/A"))
        page_label = f"Page {page_num + 1}" if isinstance(page_num, int) else f"Page {page_num}"
        sources.append(f"{source_file} ({page_label})")

    sources = list(dict.fromkeys(sources))

    return {
        "answer": answer,
        "sources": sources
    }