from typing import Literal

from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str = Field(
        description="An interview question relevant to the given topic."
    )

    difficulty: Literal["Easy", "Intermediate", "Advanced"] = Field(
        description="Difficulty level of the question."
    )

    expected_points: list[str] = Field(
        description="Key concepts expected in a good candidate's answer."
    )


class InterviewQuestionSet(BaseModel):
    topic: str = Field(
        description="The interview topic."
    )

    difficulty: Literal["Easy", "Intermediate", "Advanced"] = Field(
        description="Overall difficulty requested by the candidate."
    )

    questions: list[InterviewQuestion] = Field(
        description="Exactly five relevant interview questions."
    )