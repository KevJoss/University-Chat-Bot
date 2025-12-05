import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import TypedDict, Literal
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from src.prompts import router_prompt, response_prompt, chat_prompt
from src.tools import search_university_services

class AgentState(TypedDict):
    question: str       
    category: str       
    context: str        
    answer: str         

# --- LLLM configuration ---
llm = ChatOllama(
    model="gemma3:4b", 
    temperature=0,
    top_p=0.9,
    top_k=40)

# --- NODE DEFINITION ---
def router_node(state: AgentState):
    print(f"\n--- [DEBUG] ROUTER: Analizando '{state['question']}' ---")
    chain = router_prompt | llm | StrOutputParser()
    category = chain.invoke({"question": state["question"]})
    
    clean_category = category.strip().upper()
    if "SEARCH" in clean_category:
        clean_category = "SEARCH"
    elif "CHAT" in clean_category:
        clean_category = "CHAT"
    
    print(f"--- [DEBUG] ROUTER: Decisión tomada -> {clean_category} ---")
    return {"category": clean_category}

def search_node(state: AgentState):
    context_text = search_university_services.invoke(state["question"])
    return {"context": context_text}

def generate_node(state: AgentState):
    chain = response_prompt | llm | StrOutputParser()
    response = chain.invoke({"context": state["context"], "question": state["question"]})
    return {"answer": response}

def chat_node(state: AgentState):
    chain = chat_prompt | llm | StrOutputParser()
    response = chain.invoke({"question": state["question"]})
    return {"answer": response}

# --- GRAPH CONSTRUCTION ---

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("search", search_node)
workflow.add_node("generate", generate_node)
workflow.add_node("chat", chat_node)

# ENTRY-POINT
workflow.set_entry_point("router")

# LOGIC CONDITIONAL
def decide_next_step(state: AgentState) -> Literal["search", "chat"]:
    category = state["category"]
    if "SEARCH" in category:
        return "search"
    else:
        return "chat"

workflow.add_conditional_edges(
    "router",
    decide_next_step
)

workflow.add_edge("search", "generate")
workflow.add_edge("generate", END)
workflow.add_edge("chat", END)

# COMPILE
app = workflow.compile()

if __name__ == "__main__":
    print("\n\n>>> TEST 1: SERVICE")
    question = input("")
    inputs = {"question": question}
    result = app.invoke(inputs)
    print(f"\nRESPONSE:\n{result['answer']}")

    # Prueba 2: Saludo
    print("\n\n>>> TEST 2: GREETINGS")
    inputs = {"question": "Hola, buenos días"}
    result = app.invoke(inputs)
    print(f"\nRESPONSE:\n{result['answer']}")