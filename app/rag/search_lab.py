
from app.rag.vector_store import load_vector_store


def main():
    vector_store = load_vector_store()

    question = (
        "How can I avoid null pointer problems in Java?"
    )

    results = vector_store.similarity_search(
        query=question,
        k=3
    )

    print("\nUSER QUESTION:")
    print(question)

    print("\nTOP 3 RESULTS:")

    for index, document in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Content:", document.page_content)
        print("Metadata:", document.metadata)


if __name__ == "__main__":
    main()
