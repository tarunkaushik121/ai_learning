
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.pdf_interview_state import PDFInterviewState

from app.graph.pdf_interview_nodes import (
    retrieve_pdf_context_node,
    generate_pdf_questions_node,
    prepare_pdf_question_node,
    human_pdf_answer_node,
    evaluate_pdf_answer_node,
    advance_pdf_question_node,
    route_pdf_question,
    final_pdf_report_node,
)


def build_pdf_interview_graph(checkpointer=None):
    workflow = StateGraph(PDFInterviewState)

    workflow.add_node(
        "retrieve_pdf_context",
        retrieve_pdf_context_node
    )
    workflow.add_node(
        "generate_pdf_questions",
        generate_pdf_questions_node
    )
    workflow.add_node(
        "prepare_pdf_question",
        prepare_pdf_question_node
    )
    workflow.add_node(
        "human_pdf_answer",
        human_pdf_answer_node
    )
    workflow.add_node(
        "evaluate_pdf_answer",
        evaluate_pdf_answer_node
    )
    workflow.add_node(
        "advance_pdf_question",
        advance_pdf_question_node
    )
    workflow.add_node(
        "final_pdf_report",
        final_pdf_report_node
    )

    workflow.add_edge(
        START, "retrieve_pdf_context"
    )
    workflow.add_edge(
        "retrieve_pdf_context", "generate_pdf_questions"
    )
    workflow.add_edge(
        "generate_pdf_questions", "prepare_pdf_question"
    )
    workflow.add_edge(
        "prepare_pdf_question", "human_pdf_answer"
    )
    workflow.add_edge(
        "human_pdf_answer", "evaluate_pdf_answer"
    )
    workflow.add_edge(
        "evaluate_pdf_answer", "advance_pdf_question"
    )

    workflow.add_conditional_edges(
        "advance_pdf_question",
        route_pdf_question,
        {
            "next_question": "prepare_pdf_question",
            "finished": "final_pdf_report"
        }
    )

    workflow.add_edge("final_pdf_report", END)

    return workflow.compile(
        checkpointer=checkpointer or InMemorySaver()
    )
