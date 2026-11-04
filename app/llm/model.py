
from langchain_openai import ChatOpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL


def get_chat_model():

    model = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0.3,
        timeout=30,
        max_retries=2
    )

    return model
