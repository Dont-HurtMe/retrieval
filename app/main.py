from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.engine import engine
from app.api.routes import router
from app.api.chat import router as chat_router
from app.core.dspy_setup import configure_dspy

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_dspy()
    await engine.setup()
    yield
    await engine.close()

app = FastAPI(
    title="Search Engine & Agent API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)
app.include_router(chat_router, prefix="/api", tags=["chat"])