import json
import asyncio
from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.agent.dspy_module import KnowledgeAgent
from app.core.engine import engine

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

async def generate_chat_stream(question: str):
    try:
        retriever = engine.retriever
        if retriever is None:
            yield json.dumps({"type": "error", "content": "Search engine is still initializing..."})
            return
        agent = KnowledgeAgent(retriever=retriever)
        result = await asyncio.to_thread(agent.forward, question)
        summary_words = result.summary.split()
        for word in summary_words:
            yield json.dumps({"type": "chunk", "content": word + " "})
            await asyncio.sleep(0.02)
        refs_data = [ref.model_dump() for ref in result.references]
        yield json.dumps({"type": "references", "content": refs_data})
        yield json.dumps({"type": "done"})
    except Exception as e:
        yield json.dumps({"type": "error", "content": str(e)})

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return EventSourceResponse(generate_chat_stream(req.question))