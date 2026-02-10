import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from main import AgenticAIAssistant
import threading

# Initialize FastAPI app
app = FastAPI(
    title="Nexus AI API",
    description="REST API for interact with Nexus AI Agent",
    version="1.0.0"
)

# Initialize Agent
# We use a global instance to persist memory across requests
agent = AgenticAIAssistant()

# --- Data Models ---

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class PlanStep(BaseModel):
    step: int
    action: str
    description: str
    parameters: Optional[Dict[str, Any]] = None
    confidence: float
    reasoning: Optional[str] = None

class ExecutionResult(BaseModel):
    step: int
    action: str
    description: str
    result: Any
    status: str

class QueryResponse(BaseModel):
    query: str
    response: str
    plan: List[Dict[str, Any]]
    execution_results: List[Dict[str, Any]]

class HistoryItem(BaseModel):
    role: str
    content: str
    timestamp: str
    metadata: Dict[str, Any]

class HistoryResponse(BaseModel):
    history: List[HistoryItem]

# --- Endpoints ---

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query using Nexus AI.
    """
    try:
        # The agent.process_query is synchronous, but fast enough for this demo.
        # For production with long running tasks, we might want to use background tasks.
        result = agent.process_query(request.query, request.context)
        
        return QueryResponse(
            query=result['query'],
            response=result['response'],
            plan=result['plan'],
            execution_results=result['execution_results']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=HistoryResponse)
async def get_history(limit: int = 50):
    """
    Get conversation history.
    """
    try:
        history = agent.get_conversation_history()
        # Filter explicitly to match model just in case, though pydantic handles most
        return HistoryResponse(history=history[-limit:])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_memory")
async def clear_memory():
    """
    Clear agent memory.
    """
    try:
        agent.clear_memory()
        return {"status": "success", "message": "Memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "agent_status": "ready"}

@app.get("/kb", response_model=Dict[str, Any])
async def get_kb_content():
    """
    Get all knowledge from the agent's knowledge base.
    """
    try:
        return agent.kb.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/kb/learn")
async def learn_info(source: str, content: str):
    """
    Teach the agent new info.
    """
    try:
        agent.kb.learn(source, content)
        return {"status": "success", "message": f"Learned about {source}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

