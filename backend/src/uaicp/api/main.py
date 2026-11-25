"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from uaicp.api.knowledge import router as knowledge_router

app = FastAPI(title="Universal AI Capability Platform — Knowledge API", version="0.1.0")
app.include_router(knowledge_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}