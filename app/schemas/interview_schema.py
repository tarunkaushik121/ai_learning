
from typing import Literal

from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str = Field(
        description="An interview question."
    )

    difficulty: Literal[
        "Easy", "Intermediate", "Advanced"
    ]

    expected_points: list[str] = Field(
        description="Important concepts expected in the answer."
    )


class InterviewQuestionSet(BaseModel):
    topic: str
    difficulty: Literal[
        "Easy", "Intermediate", "Advanced"
    ]

    questions: list[InterviewQuestion]


class AnswerEvaluation(BaseModel):
    score: float = Field(
        ge=0,
        le=10,
        description="Answer score between 0 and 10."
    )

    verdict: Literal[
        "Excellent",
        "Good",
        "Average",
        "Needs Improvement"
    ]

    technical_correctness: str

    strengths: list[str]

    missing_concepts: list[str]

    improvement_suggestions: list[str]

    ideal_answer: str

    feedback_summary: str
