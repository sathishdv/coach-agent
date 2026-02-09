"""Study plan CRUD."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import StudyPlan


async def get_current_plan(db: AsyncSession, student_id: str) -> dict[str, Any] | None:
    """Return the most recent plan for a student."""
    result = await db.execute(
        select(StudyPlan)
        .where(StudyPlan.student_id == student_id)
        .order_by(StudyPlan.created_at.desc())
        .limit(1)
    )
    plan = result.scalar_one_or_none()
    return plan.to_dict() if plan else None


async def save_plan(
    db: AsyncSession,
    student_id: str,
    week_start: str,
    plan_data: dict[str, Any],
) -> dict[str, Any]:
    """Save a new weekly plan."""
    plan = StudyPlan(
        student_id=student_id,
        week_start=week_start,
        plan_data=json.dumps(plan_data),
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan.to_dict()
