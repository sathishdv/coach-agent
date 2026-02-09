"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.database import init_db
from backend.routers import attempt, chat, student, syllabus
from backend.services.notes_service import reload_notes

logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown events."""
    logger.info("Initializing database...")
    await init_db()
    logger.info("Loading notes index...")
    reload_notes()
    logger.info("JEE Coach Agent ready!")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="JEE Coach Agent",
    description="AI tutoring agent for IIT-JEE preparation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — restrictable via CORS_ORIGINS env var (default "*" for dev)
cors_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All API routes under /api prefix (kept private behind reverse proxy)
api_prefix = "/api"
app.include_router(chat.router, prefix=api_prefix)
app.include_router(student.router, prefix=api_prefix)
app.include_router(attempt.router, prefix=api_prefix)
app.include_router(syllabus.router, prefix=api_prefix)


@app.get(f"{api_prefix}/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "jee-coach-agent"}


# Serve frontend static files (for local dev; in production Nginx serves these)
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    async def serve_frontend() -> FileResponse:
        return FileResponse(str(frontend_dir / "index.html"))
