"""Attempt logging service."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Attempt


async def log_attempt(db: AsyncSession, data: dict[str, Any]) -> dict[str, Any]:
    """Log a student attempt."""
    attempt = Attempt(
        student_id=data["student_id"],
        question_id=data.get("question_id", ""),
        topic_id=data.get("topic_id", ""),
        answer=data.get("answer", ""),
        correctness=float(data.get("correctness", 0.0)),
        steps=json.dumps(data.get("steps", [])),
        time_taken=int(data.get("time_taken", 0)),
        misconception_tags=json.dumps(data.get("misconception_tags", [])),
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt.to_dict()


async def get_attempts(
    db: AsyncSession, student_id: str, limit: int = 20
) -> list[dict[str, Any]]:
    """Return recent attempts for a student."""
    result = await db.execute(
        select(Attempt)
        .where(Attempt.student_id == student_id)
        .order_by(Attempt.created_at.desc())
        .limit(limit)
    )
    return [a.to_dict() for a in result.scalars().all()]
