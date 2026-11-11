
import operator
from typing import Annotated, Any, TypedDict


class PDFInterviewState(TypedDict, total=False):
    index_id: str
    topic: str
    experience_level: str
    difficulty: str

    retrieved_context: str
    source_pages: list[int]

    questions: list[str]
    current_question_index: int
    current_question: str
    candidate_answer: str

    evaluations: Annotated[
        list[dict[str, Any]],
        operator.add
    ]

    average_score: float
