
from app.graph.interview_graph import build_interview_graph


def main():

    graph = build_interview_graph()

    initial_state = {
        "topic": "Java 8",
        "experience_level": "5 years",
        "difficulty": "Intermediate",
        "evaluations": []
    }

    result = graph.invoke(initial_state)

    print("\n===== GRAPH EXECUTION COMPLETED =====")
    print("Total evaluations:", len(result["evaluations"]))
    print("Average score:", result["average_score"])


if __name__ == "__main__":
    main()
