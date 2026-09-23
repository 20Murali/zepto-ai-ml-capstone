import os
from typing import TypedDict
from support_assistant.rag import retrieve_documents
from support_assistant.models import AskResponse
from langgraph.graph import StateGraph, START, END

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"


class GraphState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float

POLICY_KEYWORDS = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
]


def classify_intent(state: GraphState):
    query = state["query"].lower()

    if MOCK_LLM:
        if any(keyword in query for keyword in POLICY_KEYWORDS):
            intent = "policy_question"
        else:
            intent = "general_question"
    else:
        # Real LLM mode can be added later.
        # For the capstone, mock mode is the required mode.
        if any(keyword in query for keyword in POLICY_KEYWORDS):
            intent = "policy_question"
        else:
            intent = "general_question"

    return {
        "intent": intent
    }


def retrieve_and_answer(state: GraphState):
    query = state["query"]

    results = retrieve_documents(query, top_k=3)

    top_document = results["documents"][0][0]

    if MOCK_LLM:
        answer = (
            f"Based on the retrieved context: "
            f"{top_document[:200]}"
        )
    else:
        # Real LLM generation can be added later.
        answer = (
            f"Based on the retrieved context: "
            f"{top_document[:200]}"
        )

    return {
        "answer": answer,
        "sources": results["ids"][0],
        "confidence": 1.0,
    }

def direct_answer(state: GraphState):
    """Return the fixed response for general questions."""

    return {
        "answer": "I can only answer questions about Zepto policies right now.",
        "sources": [],
        "confidence": 1.0,
    }

def route_intent(state: GraphState):
    """Route the query based on the classified intent."""

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_and_answer", retrieve_and_answer)
    graph.add_node("direct_answer", direct_answer)

    graph.add_edge(START, "classify_intent")

    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer",
        },
    )

    graph.add_edge("retrieve_and_answer", END)
    graph.add_edge("direct_answer", END)

    return graph.compile()

def run_assistant(query: str) -> AskResponse:
    """Run the LangGraph assistant and return a validated response."""

    app = build_graph()

    result = app.invoke(
        {
            "query": query
        }
    )

    return AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )

# if __name__ == "__main__":
#     app = build_graph()

#     policy_result = app.invoke(
#         {
#             "query": "What is the delivery fee?"
#         }
#     )

#     print("\n--- Policy Question ---")
#     print(policy_result)

#     general_result = app.invoke(
#         {
#             "query": "What is the capital of France?"
#         }
#     )

#     print("\n--- General Question ---")
#     print(general_result)

if __name__ == "__main__":
    result = run_assistant("What is the delivery fee?")

    print(result)
    print(result.model_dump())

    