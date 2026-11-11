
from app.graph.pdf_interview_nodes import (
    retrieve_pdf_context_node
)


def main():
    index_id = input("Enter PDF index ID: ").strip()

    state = {
        "index_id": index_id,
        "topic": "Java 8",
        "experience_level": "3 years",
        "difficulty": "Intermediate"
    }

    result = retrieve_pdf_context_node(state)

    print("\nRetrieved pages:")
    print(result["source_pages"])

    print("\nRetrieved context preview:")
    print(result["retrieved_context"][:1500])


if __name__ == "__main__":
    main()
