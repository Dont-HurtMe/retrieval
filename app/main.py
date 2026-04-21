from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.engine import engine
from app.api.routes import router
from app.api.chat import router as chat_router
from app.core.dspy_setup import configure_dspy
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(chat_router, prefix="/api", tags=["chat"])