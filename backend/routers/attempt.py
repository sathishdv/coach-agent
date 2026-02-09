"""Attempt logging endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import AttemptRequest, AttemptResponse
from backend.services import attempt_service

router = APIRouter(tags=["attempt"])


@router.post("/attempt", response_model=AttemptResponse)
async def log_attempt(
    request: AttemptRequest,
    db: AsyncSession = Depends(get_db),
) -> AttemptResponse:
    """Log a student attempt."""
    data = request.model_dump()
    result = await attempt_service.log_attempt(db, data)
    return AttemptResponse(
        id=result["id"],
        student_id=result["student_id"],
        question_id=result["question_id"],
        topic_id=result["topic_id"],
        correctness=result["correctness"],
        time_taken=result["time_taken"],
        misconception_tags=result["misconception_tags"],
    )
