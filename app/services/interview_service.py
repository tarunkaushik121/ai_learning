
from langchain_core.output_parsers import StrOutputParser

from app.llm.model import get_chat_model
from app.prompts.interview_prompts import (
    topic_explanation_prompt
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
