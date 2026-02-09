"""SQLAlchemy ORM models – Postgres-ready schema on SQLite for MVP."""

from __future__ import annotations

import datetime
import json
from typing import Any

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), default="")
    email: Mapped[str] = mapped_column(String(256), default="")
    grade: Mapped[str] = mapped_column(String(16), default="")
    target_year: Mapped[int] = mapped_column(Integer, default=2026)
    strengths: Mapped[str] = mapped_column(Text, default="[]")  # JSON list
    weaknesses: Mapped[str] = mapped_column(Text, default="[]")  # JSON list
    daily_hours: Mapped[float] = mapped_column(Float, default=4.0)
    preferences: Mapped[str] = mapped_column(Text, default="{}")  # JSON
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=_now
    )

    # --- convenience helpers ---
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "grade": self.grade,
            "target_year": self.target_year,
            "strengths": json.loads(self.strengths) if self.strengths else [],
            "weaknesses": json.loads(self.weaknesses) if self.weaknesses else [],
            "daily_hours": self.daily_hours,
            "preferences": json.loads(self.preferences) if self.preferences else {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ---------------------------------------------------------------------------
# Mastery Map
# ---------------------------------------------------------------------------


class MasteryEntry(Base):
    __tablename__ = "mastery_map"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(64), index=True)
    topic_id: Mapped[str] = mapped_column(String(128))
    topic_name: Mapped[str] = mapped_column(String(256), default="")
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
    attempts_count: Mapped[int] = mapped_column(Integer, default=0)
    error_tags: Mapped[str] = mapped_column(Text, default="{}")  # JSON dict
    last_practiced: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "mastery_score": self.mastery_score,
            "attempts_count": self.attempts_count,
            "error_tags": json.loads(self.error_tags) if self.error_tags else {},
            "last_practiced": self.last_practiced.isoformat()
            if self.last_practiced
            else None,
        }


# ---------------------------------------------------------------------------
# Study Plan
# ---------------------------------------------------------------------------


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(64), index=True)
    week_start: Mapped[str] = mapped_column(String(10))  # YYYY-MM-DD
    plan_data: Mapped[str] = mapped_column(Text, default="{}")  # JSON
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "week_start": self.week_start,
            "plan_data": json.loads(self.plan_data) if self.plan_data else {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# Attempt Log
# ---------------------------------------------------------------------------


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(64), index=True)
    question_id: Mapped[str] = mapped_column(String(128), default="")
    topic_id: Mapped[str] = mapped_column(String(128), default="")
    answer: Mapped[str] = mapped_column(Text, default="")
    correctness: Mapped[float] = mapped_column(Float, default=0.0)  # 0..1
    steps: Mapped[str] = mapped_column(Text, default="[]")  # JSON
    time_taken: Mapped[int] = mapped_column(Integer, default=0)  # seconds
    misconception_tags: Mapped[str] = mapped_column(Text, default="[]")  # JSON
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "question_id": self.question_id,
            "topic_id": self.topic_id,
            "answer": self.answer,
            "correctness": self.correctness,
            "steps": json.loads(self.steps) if self.steps else [],
            "time_taken": self.time_taken,
            "misconception_tags": json.loads(self.misconception_tags)
            if self.misconception_tags
            else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# Conversation History
# ---------------------------------------------------------------------------


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(64), index=True)
    messages: Mapped[str] = mapped_column(Text, default="[]")  # JSON list
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=_now
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "messages": json.loads(self.messages) if self.messages else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
