from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager.
    Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.
    """
    print("🚀 MAS Backend starting up...")
    print("📡 Will connect to MQTT broker...")
    yield
    print("🛑 MAS Backend shutting down...")


app = FastAPI(
    title="Multi-Agent System — Elderly Care",
    description="Backend decision engine for elderly care robots",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "system": "Multi-Agent Elderly Care Backend",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "backend": "ok",
        "mqtt": "not connected yet",
        "ollama": "not connected yet"
    }