from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.engine import engine
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.setup()
    yield
    await engine.close()

app = FastAPI(
    title="DITP Search Engine API",
    description="Vector Search Engine powered by Qdrant and BGE-m3",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(router)