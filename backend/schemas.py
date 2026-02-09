"""Pydantic request/response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    student_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    plan_summary: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------


class StudentOnboardRequest(BaseModel):
    name: str = ""
    email: str = ""
    grade: str = "12"
    target_year: int = 2026
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    daily_hours: float = 4.0
    preferences: dict[str, Any] = Field(default_factory=dict)


class StudentProfile(BaseModel):
    id: str
    name: str
    email: str
    grade: str
    target_year: int
    strengths: list[str]
    weaknesses: list[str]
    daily_hours: float
    preferences: dict[str, Any]
    mastery: list[dict[str, Any]] = Field(default_factory=list)
    current_plan: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Attempt
# ---------------------------------------------------------------------------


class AttemptRequest(BaseModel):
    student_id: str
    question_id: str = ""
    topic_id: str = ""
    answer: str = ""
    correctness: float = 0.0
    steps: list[str] = Field(default_factory=list)
    time_taken: int = 0
    misconception_tags: list[str] = Field(default_factory=list)


class AttemptResponse(BaseModel):
    id: int
    student_id: str
    question_id: str
    topic_id: str
    correctness: float
    time_taken: int
    misconception_tags: list[str]


# ---------------------------------------------------------------------------
# Syllabus
# ---------------------------------------------------------------------------


class SyllabusSearchResult(BaseModel):
    topic_id: str
    topic_name: str
    subject: str
    parent_topic: str
    weight: float
