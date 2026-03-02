from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.agent import QueryRequest
from app.services.ai_agent import ask_database, stream_database

router = APIRouter()

@router.post("/ask")
async def ask_query(request: QueryRequest):
    """
    Accepts a natural language query, passes it to the AI agent 
    which runs a SQL query against the database, and returns the result.
    """
    answer = await ask_database(request.query)
    return {"query": request.query, "answer": answer}

@router.post("/stream")
async def stream_query(request: QueryRequest):
    """
    Accepts a natural language query and streams back server-sent events
    indicating agent steps and the final answer.
    """
    return StreamingResponse(
        stream_database(request.query),
        media_type="text/event-stream"
    )
