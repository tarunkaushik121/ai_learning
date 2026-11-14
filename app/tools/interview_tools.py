
from langchain.tools import tool


def create_interview_tools(report: dict):
    """
    Create a read-only tool from a completed interview report.
    """

    @tool
    def get_interview_summary() -> str:
        """Return the candidate's completed interview scores and feedback."""
        evaluations = report.get("evaluations", [])

        if not evaluations:
            return "No completed interview evaluations available."

        lines = [
            f"Average score: {report.get('average_score', 0)}/10",
            f"Questions answered: {len(evaluations)}",
        ]

        for number, item in enumerate(evaluations, start=1):
            evaluation = item["evaluation"]
            lines.append(
                f"Question {number}: {item['question']}\n"
                f"Score: {evaluation['score']}/10\n"
                f"Feedback: {evaluation['feedback']}"
            )

        return "\n\n".join(lines)

    return [get_interview_summary]
