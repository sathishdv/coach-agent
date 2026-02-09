"""Student profile endpoints."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import StudentOnboardRequest, StudentProfile
from backend.services import mastery_service, plan_service, student_service
from backend.services.coach_orchestrator import coach

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/student", tags=["student"])


@router.get("/{student_id}", response_model=StudentProfile)
async def get_student(
    student_id: str,
    db: AsyncSession = Depends(get_db),
) -> StudentProfile:
    """Get a student's full profile including mastery map and current plan."""
    student = await student_service.load_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    mastery = await mastery_service.get_mastery_map(db, student_id)
    plan = await plan_service.get_current_plan(db, student_id)

    return StudentProfile(
        id=student["id"],
        name=student["name"],
        email=student["email"],
        grade=student["grade"],
        target_year=student["target_year"],
        strengths=student["strengths"],
        weaknesses=student["weaknesses"],
        daily_hours=student["daily_hours"],
        preferences=student["preferences"],
        mastery=mastery,
        current_plan=plan.get("plan_data") if plan else None,
    )


@router.post("/{student_id}/onboard")
async def onboard_student(
    student_id: str,
    request: StudentOnboardRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Onboard a new student – creates profile and starts initial conversation."""
    try:
        # Save the student profile
        profile_data = request.model_dump()
        await student_service.upsert_student(db, student_id, profile_data)

        # Run an onboarding chat to generate initial plan
        onboarding_message = (
            f"Hi! I'm {request.name or 'a student'}. "
            f"I'm in class {request.grade}, preparing for JEE {request.target_year}. "
            f"I can study {request.daily_hours} hours daily. "
        )
        if request.strengths:
            onboarding_message += (
                f"My strong topics: {', '.join(request.strengths)}. "
            )
        if request.weaknesses:
            onboarding_message += (
                f"I need help with: {', '.join(request.weaknesses)}. "
            )
        onboarding_message += "Please create a study plan for me."

        result = await coach.chat(
            db=db,
            student_id=student_id,
            user_message=onboarding_message,
            is_onboarding=True,
        )

        return {
            "student_id": student_id,
            "message": "Student onboarded successfully",
            "coach_response": result["reply"],
            "plan_summary": result.get("plan_summary"),
        }
    except ValueError as exc:
        logger.error("Configuration error during onboarding: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error during onboarding for %s", student_id)
        raise HTTPException(
            status_code=500,
            detail=f"Onboarding failed: {exc}",
        ) from exc
