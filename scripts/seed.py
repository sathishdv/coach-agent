#!/usr/bin/env python3
"""Seed the database with sample data."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.database import async_session, init_db  # noqa: E402
from backend.services import mastery_service, plan_service, student_service  # noqa: E402


async def seed() -> None:
    """Seed the database with a sample student."""
    print("Initializing database...")
    await init_db()

    async with async_session() as db:
        # Create a sample student
        print("Creating sample student...")
        await student_service.upsert_student(
            db,
            "demo_student",
            {
                "name": "Arjun Kumar",
                "email": "arjun@example.com",
                "grade": "12",
                "target_year": 2026,
                "strengths": ["Mathematics", "Mechanics"],
                "weaknesses": ["Organic Chemistry", "Thermodynamics"],
                "daily_hours": 5.0,
                "preferences": {"style": "problem-solving", "pace": "moderate"},
            },
        )

        # Seed some mastery data
        print("Seeding mastery map...")
        await mastery_service.update_mastery(
            db,
            "demo_student",
            [
                {
                    "topic_id": "ph_kinematics",
                    "topic_name": "Kinematics",
                    "mastery_score": 0.75,
                    "delta_attempts": 15,
                },
                {
                    "topic_id": "ph_newtons_laws",
                    "topic_name": "Newton's Laws of Motion",
                    "mastery_score": 0.65,
                    "delta_attempts": 12,
                },
                {
                    "topic_id": "ma_differentiation",
                    "topic_name": "Differentiation",
                    "mastery_score": 0.80,
                    "delta_attempts": 20,
                },
                {
                    "topic_id": "ma_integration",
                    "topic_name": "Indefinite Integration",
                    "mastery_score": 0.55,
                    "delta_attempts": 10,
                },
                {
                    "topic_id": "ch_goc",
                    "topic_name": "General Organic Chemistry",
                    "mastery_score": 0.30,
                    "delta_attempts": 8,
                },
                {
                    "topic_id": "ch_thermodynamics",
                    "topic_name": "Chemical Thermodynamics",
                    "mastery_score": 0.25,
                    "delta_attempts": 5,
                },
            ],
        )

        # Seed a sample study plan
        print("Seeding study plan...")
        await plan_service.save_plan(
            db,
            "demo_student",
            "2026-02-09",
            {
                "week_number": 1,
                "focus": "Strengthen weak areas + maintain strong topics",
                "daily_tasks": {
                    "Monday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Organic Chemistry: GOC concepts revision",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Practice 15 GOC problems",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Integration techniques",
                            "topic_id": "ma_integration",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Kinematics problem set (maintain)",
                            "topic_id": "ph_kinematics",
                        },
                    ],
                    "Tuesday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Chemical Thermodynamics: First & Second Law",
                            "topic_id": "ch_thermodynamics",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Practice thermodynamics numericals",
                            "topic_id": "ch_thermodynamics",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Newton's Laws revision + problems",
                            "topic_id": "ph_newtons_laws",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Differentiation advanced problems",
                            "topic_id": "ma_differentiation",
                        },
                    ],
                    "Wednesday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Organic Chemistry: Reaction mechanisms",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Mixed practice set (GOC + Thermodynamics)",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Integration by parts & partial fractions",
                            "topic_id": "ma_integration",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Physics: Rotational mechanics intro",
                            "topic_id": "ph_rotational",
                        },
                    ],
                    "Thursday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Chemical Thermodynamics: Hess's law problems",
                            "topic_id": "ch_thermodynamics",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Mini test: Thermodynamics (45 min)",
                            "topic_id": "ch_thermodynamics",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Newton's Laws: Friction & circular motion",
                            "topic_id": "ph_newtons_laws",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Definite integration practice",
                            "topic_id": "ma_definite_integration",
                        },
                    ],
                    "Friday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Organic Chemistry: Named reactions",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Practice set: Mixed organic",
                            "topic_id": "ch_goc",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Revision: Week's weak points",
                            "topic_id": "",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Mock test: 30 questions mixed",
                            "topic_id": "",
                        },
                    ],
                    "Saturday": [
                        {
                            "time": "09:00-12:00",
                            "task": "Full-length practice test (3 hours)",
                            "topic_id": "",
                        },
                        {
                            "time": "14:00-15:30",
                            "task": "Test analysis and error review",
                            "topic_id": "",
                        },
                        {
                            "time": "15:45-17:00",
                            "task": "Revise formulas and key concepts",
                            "topic_id": "",
                        },
                    ],
                    "Sunday": [
                        {
                            "time": "09:00-10:30",
                            "task": "Light revision: Formula sheets",
                            "topic_id": "",
                        },
                        {
                            "time": "10:45-12:00",
                            "task": "Doubt clearing session / backlog",
                            "topic_id": "",
                        },
                    ],
                },
                "spaced_repetition": [
                    {
                        "topic_id": "ph_kinematics",
                        "next_review": "2026-02-12",
                        "interval_days": 3,
                    },
                    {
                        "topic_id": "ma_differentiation",
                        "next_review": "2026-02-14",
                        "interval_days": 5,
                    },
                ],
            },
        )

    print("Seed data created successfully!")
    print("  - Student: demo_student (Arjun Kumar)")
    print("  - Mastery entries: 6 topics")
    print("  - Study plan: Week of 2026-02-09")


if __name__ == "__main__":
    asyncio.run(seed())
