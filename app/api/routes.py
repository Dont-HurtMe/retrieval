from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.schemas import SearchRequest, SearchResponse, IndexRequest
from app.services.retriever import execute_search
from app.services.indexer import process_and_index_document

router = APIRouter()

@router.post("/api/search", response_model=SearchResponse)
async def search_knowledge(req: SearchRequest):
    try:
        result = await execute_search(query=req.query, top_k=req.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/index")
async def index_document(req: IndexRequest, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(
        process_and_index_document, 
        req.doc_id,
        req.provider,
        req.filename,
        req.raw_storage_path,
        req.parquet_storage_path
    )
    return {"status": "accepted", "message": f"Added {req.doc_id} to indexing queue."}