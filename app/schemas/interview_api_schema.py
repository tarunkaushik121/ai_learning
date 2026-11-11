
from enum import Enum
from uuid import UUID
from typing import Any, Literal
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator
)


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class StartInterviewRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    topic: str = Field(
        min_length=2,
        max_length=100,
        examples=["Java 8"]
    )

    experience_level: str = Field(
        min_length=1,
        max_length=50,
        examples=["5 years"]
    )

    difficulty: DifficultyLevel = Field(
        description=(
            "1/Easy, 2/Medium/Intermediate, "
            "3/Advanced"
        )
    )

    @field_validator("difficulty", mode="before")
    @classmethod
    def normalize_difficulty(cls, value):

        if isinstance(value, DifficultyLevel):
            return value

        mapping = {
            "1": "Easy",
            "easy": "Easy",

            "2": "Intermediate",
            "medium": "Intermediate",
            "intermediate": "Intermediate",

            "3": "Advanced",
            "advanced": "Advanced"
        }

        normalized = str(value).strip().lower()

        return mapping.get(normalized, value)


class StartInterviewResponse(BaseModel):

    thread_id: UUID
    status: str
    topic: str
    question_number: int = Field(ge=1)
    question: str



class SubmitAnswerRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    answer: str = Field(
        min_length=1,
        max_length=10000,
        description="Candidate's answer",
        examples=[
            "A functional interface contains exactly "
            "one abstract method."
        ]
    )


class SubmitAnswerResponse(BaseModel):

    thread_id: UUID

    status: Literal[
        "waiting_for_answer",
        "completed"
    ]

    evaluated_question: str
    submitted_answer: str

    evaluation: dict[str, Any]

    next_question_number: int | None = None
    next_question: str | None = None

    average_score: float | None = None
    total_questions: int | None = None
