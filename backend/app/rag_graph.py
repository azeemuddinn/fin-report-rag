from typing import List, TypedDict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END


# 1. Define the Graph State schema
class GraphState(TypedDict):
    question: str
    documents: List[Document]
    generation: str
    web_search_needed: str


def create_rag_graph(retriever, llm):
    
    # --- Nodes ---
    
    def retrieve_node(state: GraphState):
        """Fetch documents from Supabase vector store retriever."""
        question = state["question"]
        docs = retriever.invoke(question)
        return {"documents": docs, "question": question}

    def grade_documents_node(state: GraphState):
        """Grade whether retrieved chunks are relevant to the question."""
        question = state["question"]
        docs = state["documents"]

        # Use a fast evaluator prompt
        grading_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a strict financial document grader assessing whether a retrieved document chunk contains information relevant to answering the user's question. Answer only 'yes' or 'no'."),
            ("human", "Question: {question}\n\nDocument Chunk:\n{context}\n\nIs this chunk relevant? (yes/no)")
        ])
        
        eval_chain = grading_prompt | llm | StrOutputParser()
        
        relevant_docs = []
        web_search = "no"
        
        for doc in docs:
            score = eval_chain.invoke({"question": question, "context": doc.page_content})
            if "yes" in score.lower():
                relevant_docs.append(doc)
                
        # If no chunks are relevant, flag for fallback / web search routing
        if not relevant_docs:
            web_search = "yes"
            
        return {"documents": relevant_docs or docs, "web_search_needed": web_search}

    def generate_node(state: GraphState):
        """Generate final financial response using the resilient chain."""
        question = state["question"]
        docs = state["documents"]
        
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        generation_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert financial analyst assistant. Answer the user's question strictly using the provided context."),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])
        
        generation_chain = generation_prompt | llm | StrOutputParser()
        generation = generation_chain.invoke({"context": context_text, "question": question})
        
        return {"generation": generation}

    # --- Conditional Router ---
    
    def decide_to_generate(state: GraphState):
        """Route depending on document relevance grading."""
        if state.get("web_search_needed") == "yes":
            # Can route to a web search node or fallback response
            return "generate" 
        return "generate"

    # --- Build the State Graph ---
    
    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("generate", generate_node)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "generate": "generate",
        },
    )
    workflow.add_edge("generate", END)

    return workflow.compile()