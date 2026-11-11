
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.interview_state import InterviewState
from app.graph.interview_nodes import (
    generate_questions_node,
    prepare_question_node,
    human_answer_node,
    evaluate_answer_node,
    advance_question_node,
    route_next_question,
    final_report_node
)


def build_interview_graph(checkpointer=None):

    builder = StateGraph(InterviewState)

    builder.add_node(
        "generate_questions",
        generate_questions_node
    )

    builder.add_node(
        "prepare_question",
        prepare_question_node
    )

    builder.add_node(
        "human_answer",
        human_answer_node
    )

    builder.add_node(
        "evaluate_answer",
        evaluate_answer_node
    )

    builder.add_node(
        "advance_question",
        advance_question_node
    )

    builder.add_node(
        "final_report",
        final_report_node
    )

    builder.add_edge(START, "generate_questions")

    builder.add_edge(
        "generate_questions",
        "prepare_question"
    )

    builder.add_edge(
        "prepare_question",
        "human_answer"
    )

    builder.add_edge(
        "human_answer",
        "evaluate_answer"
    )

    builder.add_edge(
        "evaluate_answer",
        "advance_question"
    )

    builder.add_conditional_edges(
        "advance_question",
        route_next_question,
        {
            "continue": "prepare_question",
            "finish": "final_report"
        }
    )

    builder.add_edge("final_report", END)

    if checkpointer is None:
        checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)
