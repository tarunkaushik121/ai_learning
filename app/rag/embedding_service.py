
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Create the embedding model used by our RAG pipeline.
    """

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing from .env"
        )

    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )


def main():
    embeddings = get_embedding_model()

    text = "Java 8 introduced lambda expressions."

    vector = embeddings.embed_query(text)

    print("Original text:", text)
    print("Vector dimensions:", len(vector))
    print("First 10 values:", vector[:10])


if __name__ == "__main__":
    main()
