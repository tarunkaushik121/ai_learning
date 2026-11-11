
from app.llm.model import get_chat_model

from app.schemas.interview_schema import (
    InterviewQuestionSet,
    AnswerEvaluation
)

from app.prompts.interview_prompts import (
    topic_explanation_prompt,
    question_generation_prompt,
    answer_evaluation_prompt
)

from langchain_core.output_parsers import StrOutputParser


def explain_topic(
    topic: str,
    experience_level: str,
    difficulty: str
) -> str:

    model = get_chat_model()

    chain = (
        topic_explanation_prompt
        | model
        | StrOutputParser()
    )

    result = chain.invoke({
        "topic": topic,
        "experience_level": experience_level,
        "difficulty": difficulty
    })

    return result


def generate_questions(
    topic: str,
    experience_level: str,
    difficulty: str
) -> InterviewQuestionSet:

    model = get_chat_model()

    structured_model = model.with_structured_output(
        InterviewQuestionSet
    )

    chain = question_generation_prompt | structured_model

    result = chain.invoke({
        "topic": topic,
        "experience_level": experience_level,
        "difficulty": difficulty
    })

    if len(result.questions) != 5:
        raise ValueError(
            f"Expected 5 questions, received {len(result.questions)}"
        )

    return result


def evaluate_answer(
    question: str,
    candidate_answer: str,
    experience_level: str
) -> AnswerEvaluation:

    model = get_chat_model()

    structured_model = model.with_structured_output(
        AnswerEvaluation
    )

    chain = answer_evaluation_prompt | structured_model

    result = chain.invoke({
        "question": question,
        "candidate_answer": candidate_answer,
        "experience_level": experience_level
    })

    return result
