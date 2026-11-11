"""API route contracts for multi-agent query and SSE streaming."""
import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.app.schemas.chat import QueryRequest, ChatResponse
from backend.app.schemas.citation import Citation

router = APIRouter(prefix="/chat", tags=["Chat"])

async def mock_sse_generator(request: QueryRequest):
    """Mock SSE stream emitting agent events and citation tokens."""
    events = [
        {"event": "agent_status", "data": {"agent": "RetrievalAgent", "status": "searching chunks"}},
        {"event": "agent_status", "data": {"agent": "AnalysisAgent", "status": "synthesizing response"}},
        {"event": "token", "data": {"chunk": "According to the retrieved papers, "}},
        {"event": "token", "data": {"chunk": "the proposed methodology relies on self-attention."}},
        {
            "event": "citation",
            "data": {
                "paper_id": request.paper_ids[0] if request.paper_ids else "paper-default",
                "paper_title": "Source Document",
                "page_number": 1,
                "quote": "the proposed methodology relies on self-attention."
            }
        },
        {"event": "done", "data": {"status": "completed"}}
    ]
    for ev in events:
        yield f"event: {ev['event']}\ndata: {json.dumps(ev['data'])}\n\n"
        await asyncio.sleep(0.01)

@router.post("/query")
async def query_chat(request: QueryRequest):
    """Submit natural language research query against indexed papers."""
    if request.stream:
        return StreamingResponse(
            mock_sse_generator(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    return ChatResponse(
        answer="According to the retrieved papers, the proposed methodology relies on self-attention.",
        citations=[
            Citation(
                paper_id=request.paper_ids[0] if request.paper_ids else "paper-default",
                paper_title="Source Document",
                page_number=1,
                quote="the proposed methodology relies on self-attention."
            )
        ],
        research_gaps=[]
    )
