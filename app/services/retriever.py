from app.core.engine import engine
from app.models.schemas import SearchResponse, SearchResult

async def execute_search(query: str, top_k: int) -> SearchResponse:
    if not engine.retriever:
        raise ValueError("Search engine is not ready.")
    engine.retriever.similarity_top_k = top_k
    results = await engine.retriever.aretrieve(query)
    formatted_results = []
    for res in results:
        score = round(res.score, 4) if res.score is not None else 0.0
        
        formatted_results.append(SearchResult(
            score=score,
            text=res.text,
            metadata=res.metadata
        ))
    return SearchResponse(query=query, results=formatted_results)