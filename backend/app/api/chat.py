"""API routes for multi-agent query and SSE streaming."""
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.app.schemas.chat import QueryRequest, ChatResponse
from backend.app.agents.orchestrator import ResearchWorkflow
from backend.app.api.papers import get_retriever

router = APIRouter(prefix="/chat", tags=["Chat"])

async def sse_event_generator(request: QueryRequest):
    workflow = ResearchWorkflow(retriever=get_retriever())
    async for event in workflow.stream_workflow(
        query=request.query,
        paper_ids=request.paper_ids if request.paper_ids else None,
        top_k=request.top_k
    ):
        yield f"event: {event['event']}\ndata: {json.dumps(event['data'])}\n\n"

@router.post("/query")
async def query_chat(request: QueryRequest):
    """Submit natural language research query against indexed papers."""
    if request.stream:
        return StreamingResponse(
            sse_event_generator(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    workflow = ResearchWorkflow(retriever=get_retriever())
    result = await workflow.run(
        query=request.query,
        paper_ids=request.paper_ids if request.paper_ids else None,
        top_k=request.top_k
    )
    return ChatResponse(
        answer=result["answer"],
        citations=result["citations"],
        research_gaps=result["research_gaps"],
        comparison_matrix=result["comparison_matrix"]
    )
