
from typing import Literal

from pydantic import BaseModel, Field


# Milestone 2: Question Generator Schema

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


# Milestone 3: Answer Evaluation Schema

class AnswerEvaluation(BaseModel):

    score: float = Field(
        ge=0,
        le=10,
        description="Overall answer score between 0 and 10."
    )

    verdict: Literal[
        "Excellent",
        "Good",
        "Average",
        "Needs Improvement"
    ] = Field(
        description="Overall assessment of the candidate's answer."
    )

    technical_correctness: str = Field(
        description="Evaluate technical accuracy of the answer."
    )

    strengths: list[str] = Field(
        description="Concepts correctly explained by the candidate."
    )

    missing_concepts: list[str] = Field(
        description="Important concepts missing from the answer."
    )

    improvement_suggestions: list[str] = Field(
        description="Actionable suggestions to improve the answer."
    )

    ideal_answer: str = Field(
        description="A technically accurate, interview-ready answer."
    )

    feedback_summary: str = Field(
        description="Short summary of the overall evaluation."
    )
