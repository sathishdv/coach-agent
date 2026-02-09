"""CRUD operations for students."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Student


async def load_student(db: AsyncSession, student_id: str) -> dict[str, Any] | None:
    """Load a student by ID. Returns dict or None."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    return student.to_dict() if student else None


async def upsert_student(
    db: AsyncSession, student_id: str, data: dict[str, Any]
) -> dict[str, Any]:
    """Create or update a student profile."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()

    if student is None:
        student = Student(id=student_id)
        db.add(student)

    if "name" in data:
        student.name = data["name"]
    if "email" in data:
        student.email = data["email"]
    if "grade" in data:
        student.grade = str(data["grade"])
    if "target_year" in data:
        student.target_year = int(data["target_year"])
    if "strengths" in data:
        student.strengths = (
            json.dumps(data["strengths"])
            if isinstance(data["strengths"], list)
            else data["strengths"]
        )
    if "weaknesses" in data:
        student.weaknesses = (
            json.dumps(data["weaknesses"])
            if isinstance(data["weaknesses"], list)
            else data["weaknesses"]
        )
    if "daily_hours" in data:
        student.daily_hours = float(data["daily_hours"])
    if "preferences" in data:
        student.preferences = (
            json.dumps(data["preferences"])
            if isinstance(data["preferences"], dict)
            else data["preferences"]
        )

    await db.commit()
    await db.refresh(student)
    return student.to_dict()
