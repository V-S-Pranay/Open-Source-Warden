"""FastAPI entry point for Open-Source-Warden."""

import logging

from fastapi import FastAPI

from app.config import settings
from app.logging_config import setup_logging
from app.webhook import router as webhook_router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Open-Source-Warden",
    description=(
        "AI-powered GitHub assistant for open-source maintainers, "
        "powered by NVIDIA Llama-3.3-Nemotron-Super-49B"
    ),
    version="1.0.0",
)

app.include_router(webhook_router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint used by Docker and load balancers."""
    return {"status": "ok", "model": settings.NVIDIA_MODEL}


@app.get("/")
async def root() -> dict:
    """Root endpoint with app metadata."""
    return {
        "name": "Open-Source-Warden",
        "powered_by": "NVIDIA Nemotron-3-Super",
        "docs": "/docs",
    }
