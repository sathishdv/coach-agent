"""Syllabus search endpoint."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from backend.services import syllabus_service

router = APIRouter(prefix="/syllabus", tags=["syllabus"])


@router.get("/search")
async def search_syllabus(
    q: str = Query(..., description="Search query"),
) -> list[dict[str, Any]]:
    """Search the JEE syllabus by keyword."""
    return syllabus_service.search_syllabus(q)


@router.get("/full")
async def get_full_syllabus() -> dict[str, Any]:
    """Return the complete JEE syllabus."""
    return syllabus_service.get_full_syllabus()
