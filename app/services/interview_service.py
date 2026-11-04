from app.llm.model import get_chat_model
from app.prompts.interview_prompts import question_generation_prompt
from app.schemas.interview_schema import InterviewQuestionSet
from langchain_core.output_parsers import StrOutputParser
from app.prompts.interview_prompts import answer_evaluation_prompt
from app.schemas.interview_schema import AnswerEvaluation
from app.llm.model import get_chat_model
from app.prompts.interview_prompts import (
    topic_explanation_prompt
)
from app.llm.model import get_chat_model

from app.prompts.interview_prompts import (
    topic_explanation_prompt,
    question_generation_prompt,
    answer_evaluation_prompt
)

from app.schemas.interview_schema import (
    InterviewQuestionSet,
    AnswerEvaluation
)


def explain_topic(
    topic: str,
    experience_level: str,
    difficulty: str
) -> str:

    model = get_chat_model()

    # Build a modern LangChain runnable pipeline
    chain = (
        topic_explanation_prompt
        | model
        | StrOutputParser()
    )

    # Execute the pipeline
    result = chain.invoke(
        {
            "topic": topic,
            "experience_level": experience_level,
            "difficulty": difficulty
        }
    )

    return result

def generate_questions(
    topic: str,
    experience_level: str,
    difficulty: str
) -> InterviewQuestionSet:

    # Step 1: Get the configured LLM
    model = get_chat_model()

    # Step 2: Tell the LLM to return an InterviewQuestionSet object
    structured_model = model.with_structured_output(
        InterviewQuestionSet
    )

    # Step 3: Create the LangChain pipeline
    chain = question_generation_prompt | structured_model

    # Step 4: Execute the pipeline
    result = chain.invoke(
        {
            "topic": topic,
            "experience_level": experience_level,
            "difficulty": difficulty
        }
    )

    # Step 5: Validate the number of questions
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

    # Step 1: Get configured LLM
    model = get_chat_model()

    # Step 2: Configure structured output
    structured_model = model.with_structured_output(
        AnswerEvaluation
    )

    # Step 3: Build LangChain pipeline
    chain = answer_evaluation_prompt | structured_model

    # Step 4: Execute pipeline
    result = chain.invoke(
        {
            "question": question,
            "candidate_answer": candidate_answer,
            "experience_level": experience_level
        }
    )

    # Step 5: Return validated Pydantic object
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

    result = chain.invoke(
        {
            "question": question,
            "candidate_answer": candidate_answer,
            "experience_level": experience_level
        }
    )

    return result