import torch
from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams
from llama_index.core import VectorStoreIndex, Settings as LlamaSettings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.core.config import settings

class SearchEngine:
    def __init__(self):
        self.client: QdrantClient | None = None
        self.aclient: AsyncQdrantClient | None = None
        self.index: VectorStoreIndex | None = None
        self.retriever = None
    async def setup(self):
        print(f"🚀 [Engine] Initializing model: {settings.model_name}")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        LlamaSettings.embed_model = HuggingFaceEmbedding(
            model_name=settings.model_name, 
            device=device
        )
        LlamaSettings.llm = None
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        self.aclient = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        v_size = 384 if "MiniLM" in settings.model_name else 1024
        if not await self.aclient.collection_exists(settings.collection_name):
            try:
                print(f"📦 [Engine] Creating collection: {settings.collection_name} (Size: {v_size})")
                await self.aclient.create_collection(
                    collection_name=settings.collection_name,
                    vectors_config=VectorParams(size=v_size, distance=Distance.COSINE),
                )
            except Exception as e:
                if "already exists" in str(e).lower() or "409" in str(e):
                    print("⚠️ [Engine] Collection already created. Skipping.")
                else:
                    raise e
        vector_store = QdrantVectorStore(
            client=self.client,   
            aclient=self.aclient, 
            collection_name=settings.collection_name
        )
        self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        self.retriever = self.index.as_retriever(similarity_top_k=5)
        print("✅ [Engine] Setup complete. Ready to serve!")
    async def close(self):
        if self.aclient:
            await self.aclient.close()

engine = SearchEngine()