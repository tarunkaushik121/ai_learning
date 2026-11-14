
from langchain.tools import tool

from app.rag.pdf_indexer import load_pdf_index


def create_pdf_tools(index_id: str):
    """
    Build tools scoped to one trusted PDF index.
    The LLM cannot choose an arbitrary index path.
    """

    @tool
    def search_pdf_knowledge(query: str) -> str:
        """Search the candidate's indexed PDF for technical facts."""
        if not query.strip():
            return "Please provide a search query."

        store = load_pdf_index(index_id)

        documents = store.similarity_search(
            query=query,
            k=3
        )

        if not documents:
            return "No PDF content found."

        results = []

        for doc in documents:
            page = doc.metadata.get("page", 0) + 1
            results.append(
                f"Page {page}:\n{doc.page_content}"
            )

        return "\n\n".join(results)

    @tool
    def explain_java_concept(topic: str) -> str:
        """Retrieve PDF material useful for explaining a Java concept."""
        if not topic.strip():
            return "Please provide a Java topic."

        store = load_pdf_index(index_id)

        documents = store.similarity_search(
            query=f"Explain Java concept: {topic}",
            k=3
        )

        if not documents:
            return "No supporting explanation found."

        return "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}: "
            f"{doc.page_content}"
            for doc in documents
        )

    return [search_pdf_knowledge, explain_java_concept]
