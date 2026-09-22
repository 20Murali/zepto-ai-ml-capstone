from fastapi import FastAPI

from support_assistant.graph import run_assistant
from support_assistant.models import AskRequest, AskResponse


app = FastAPI(
    title="Zepto Support Assistant",
    description="RAG-based Zepto policy support assistant",
    version="1.0.0",
)


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return run_assistant(request.query)