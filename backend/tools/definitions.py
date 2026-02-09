"""Claude tool definitions for the Coach Agent."""

from __future__ import annotations

TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "load_student",
        "description": (
            "Load a student's full profile including name, grade, strengths, "
            "weaknesses, daily study hours, and preferences."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Unique student identifier.",
                }
            },
            "required": ["student_id"],
        },
    },
    {
        "name": "upsert_student",
        "description": (
            "Create or update a student's profile/state. "
            "Use this after onboarding or when the student provides new info."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
                "profile": {
                    "type": "object",
                    "description": "Student profile fields to set/update.",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "grade": {"type": "string"},
                        "target_year": {"type": "integer"},
                        "strengths": {"type": "array", "items": {"type": "string"}},
                        "weaknesses": {"type": "array", "items": {"type": "string"}},
                        "daily_hours": {"type": "number"},
                        "preferences": {"type": "object"},
                    },
                },
            },
            "required": ["student_id", "profile"],
        },
    },
    {
        "name": "log_attempt",
        "description": (
            "Log a student's attempt at a question. Records answer, correctness, "
            "steps taken, time, and any misconception tags."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
                "attempt": {
                    "type": "object",
                    "properties": {
                        "question_id": {"type": "string"},
                        "topic_id": {"type": "string"},
                        "answer": {"type": "string"},
                        "correctness": {
                            "type": "number",
                            "description": "Score between 0 and 1.",
                        },
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Steps the student took.",
                        },
                        "time_taken": {
                            "type": "integer",
                            "description": "Seconds taken.",
                        },
                        "misconception_tags": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["student_id", "topic_id"],
                },
            },
            "required": ["student_id", "attempt"],
        },
    },
    {
        "name": "update_mastery",
        "description": (
            "Update the student's mastery map for one or more topics. "
            "Call this after evaluating an attempt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
                "topic_updates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic_id": {"type": "string"},
                            "topic_name": {"type": "string"},
                            "mastery_score": {
                                "type": "number",
                                "description": "New mastery score 0..1.",
                            },
                            "error_tags": {
                                "type": "object",
                                "description": "Map of error tag -> count increment.",
                            },
                            "delta_attempts": {
                                "type": "integer",
                                "description": "Number of new attempts to add.",
                            },
                        },
                        "required": ["topic_id"],
                    },
                },
            },
            "required": ["student_id", "topic_updates"],
        },
    },
    {
        "name": "get_syllabus",
        "description": (
            "Search the JEE syllabus for topics matching a query. "
            "Returns matching topics with subject, parent topic, and weight."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g. 'kinematics', 'organic', 'calculus').",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "search_notes",
        "description": (
            "Search curated JEE study notes using keyword search. "
            "Returns relevant note sections with formulas, concepts, and tips."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g. 'Newton laws', 'SN2 reaction').",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "generate_practice_set",
        "description": (
            "Generate a set of JEE-style practice questions. "
            "Returns questions with options, hints, and solutions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of topic IDs or names.",
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["easy", "medium", "hard", "mixed"],
                    "description": "Difficulty level.",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of questions to generate.",
                },
                "format": {
                    "type": "string",
                    "enum": ["mcq", "numerical", "subjective", "mixed"],
                    "description": "Question format.",
                },
            },
            "required": ["topics", "difficulty", "count"],
        },
    },
    {
        "name": "generate_test_blueprint",
        "description": (
            "Generate a test/mock exam blueprint with time allocation, "
            "topic distribution, and difficulty mix."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "duration_min": {
                    "type": "integer",
                    "description": "Total test duration in minutes.",
                },
                "topics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Topics to include.",
                },
                "difficulty_mix": {
                    "type": "object",
                    "description": 'Distribution, e.g. {"easy": 0.3, "medium": 0.5, "hard": 0.2}.',
                },
            },
            "required": ["duration_min", "topics"],
        },
    },
    {
        "name": "get_mastery_map",
        "description": "Retrieve the student's current mastery map for all topics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
            },
            "required": ["student_id"],
        },
    },
    {
        "name": "get_study_plan",
        "description": "Retrieve the student's current weekly study plan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
            },
            "required": ["student_id"],
        },
    },
    {
        "name": "save_study_plan",
        "description": "Save a new weekly study plan for the student.",
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string"},
                "week_start": {
                    "type": "string",
                    "description": "ISO date of the week start, e.g. '2026-02-09'.",
                },
                "plan_data": {
                    "type": "object",
                    "description": "Full weekly plan with daily tasks, time boxes, etc.",
                },
            },
            "required": ["student_id", "week_start", "plan_data"],
        },
    },
]
