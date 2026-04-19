from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="คำถามที่ต้องการค้นหา")
    top_k: int = Field(default=5, description="จำนวน Chunk ที่ต้องการให้คืนค่า")

class IndexRequest(BaseModel):
    doc_id: str
    provider: str
    filename: str
    raw_storage_path: str
    parquet_storage_path: str

class ChunkMetadata(BaseModel):
    doc_id: str
    provider: str
    filename: str
    page_number: int
    raw_storage_path: str

class SearchResult(BaseModel):
    score: float
    text: str
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]