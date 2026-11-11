
from typing import TypedDict, NotRequired, Annotated, Any
import operator


class InterviewState(TypedDict):

    topic: str
    experience_level: str
    difficulty: str

    questions: NotRequired[list[dict[str, Any]]]

    current_question_index: NotRequired[int]

    current_question: NotRequired[str]

    candidate_answer: NotRequired[str]

    # Reducer: append new evaluations to existing history
    evaluations: Annotated[
        list[dict[str, Any]],
        operator.add
    ]

    average_score: NotRequired[float]

