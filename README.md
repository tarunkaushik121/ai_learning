LangGraph Interview Workflow — Practical Learning Guide
Project: AI Interview Assistant
Branch: feature/langgraph-workflow (keep separate from main)
Status: Labs 5.1–5.4 implemented; persistent checkpointing deferred.

1. Why LangGraph?
LangChain provides model integrations, prompt templates, structured output, and reusable AI services. LangGraph coordinates those services as a stateful workflow. Our application generates five interview questions, presents them one at a time, waits for human answers, evaluates each answer, and calculates a final report.

Think of LangGraph as a workflow engine around existing service functions—not a replacement for them. In Spring Boot terms, the existing LangChain service functions resemble business services; graph nodes invoke those services; edges define orchestration; graph state resembles a workflow DTO.
2. Architecture
START
  |
  v
generate_questions
  |
  v
prepare_question <------------------------+
  |                                        |
  v                                        |
human_answer (interrupt)                   |
  |                                        |
  | Command(resume=answer)                 |
  v                                        |
evaluate_answer                            |
  |                                        |
  v                                        |
advance_question                           |
  |                                        |
  +-- more questions ----------------------+ 
  |
  +-- finished --> final_report --> END
Source files
app/
  graph/
    __init__.py
    interview_state.py       # Shared workflow state and reducer
    interview_nodes.py       # Node functions and routing
    interview_graph.py       # StateGraph definition and compilation
  langgraph_interactive.py   # CLI driving interrupt/resume
  langgraph_demo.py          # Earlier demo; may require adjustment
  services/
    interview_service.py     # Existing LangChain services
  schemas/
    interview_schema.py      # Pydantic output models
3. Environment and commands
From the project root in Windows PowerShell:
.\.venv\Scripts\Activate.ps1
python -m pip install -U "langgraph>=1.0,<2.0"
python -m app.langgraph_interactive
Keep your model API key in environment variables or a locally ignored .env file. Never commit API keys, .env, .venv, or database files. Check .gitignore before pushing.
4. Graph state: InterviewState
A TypedDict declares the keys that nodes read and update. NotRequired allows keys to be absent until the appropriate node populates them.
from typing import TypedDict, NotRequired, Annotated, Any
import operator

class InterviewState(TypedDict):
    topic: str
    experience_level: str
    difficulty: str
    questions: NotRequired[list[dict[str, Any]]]
    current_question_index: NotRequired[int]
    current_question: NotRequired[str]
    candidate_answer: NotRequired[str]
    evaluations: Annotated[list[dict[str, Any]], operator.add]
    average_score: NotRequired[float]
Crucial: evaluations has a reducer. Without Annotated[..., operator.add], each update replaces the previous list. With it, each node's returned list is appended to existing state.

Initialize the graph with "evaluations": [] once. An evaluation node should return only its new item:
return {"evaluations": [{
    "question": question,
    "candidate_answer": candidate_answer,
    "evaluation": result.model_dump(),
}]}
Do not return state["evaluations"] + [new_item] when using the reducer: that duplicates the old history. Do not reset evaluations in generate_questions_node.
Small reducer example
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    values: Annotated[list[int], operator.add]

def one(state: S): return {"values": [4]}
def two(state: S): return {"values": [0]}
def three(state: S): return {"values": [2]}

builder = StateGraph(S)
builder.add_node("one", one)
builder.add_node("two", two)
builder.add_node("three", three)
builder.add_edge(START, "one")
builder.add_edge("one", "two")
builder.add_edge("two", "three")
builder.add_edge("three", END)
result = builder.compile().invoke({"values": []})
assert result["values"] == [4, 0, 2]
5. Nodes and edges
A node is a Python function receiving the current state and returning a dictionary of state updates. Avoid mutating the input state directly. The graph composes the nodes.
Node	Responsibility	Typical updates
generate_questions_node	Call existing question-generation service	questions, current_question_index=0
prepare_question_node	Select question at current index	current_question
human_answer_node	Pause for candidate response	candidate_answer after resume
evaluate_answer_node	Call existing structured evaluator	evaluations: [new_evaluation]
advance_question_node	Increment index	current_question_index
final_report_node	Calculate score average	average_score


Edges define order. Conditional edges choose the next node:
def route_next_question(state):
    return (
        "continue"
        if state["current_question_index"] < len(state["questions"])
        else "finish"
    )

builder.add_conditional_edges(
    "advance_question",
    route_next_question,
    {"continue": "prepare_question", "finish": "final_report"},
)
After the fifth question, index becomes 5; because 5 < 5 is false, the graph proceeds to final_report.
6. Human-in-the-loop: interrupt and resume
interrupt() is not the same as input(). It pauses the graph and returns a payload to the caller. The caller collects input and resumes the graph with Command(resume=...).
from langgraph.types import interrupt

def human_answer_node(state: InterviewState) -> dict:
    answer = interrupt({
        "question_number": state["current_question_index"] + 1,
        "question": state["current_question"],
        "message": "Please provide your interview answer.",
    })
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Candidate answer must be a nonempty string")
    return {"candidate_answer": answer.strip()}
The CLI controls the interaction:
from uuid import uuid4
from langgraph.types import Command

thread_id = str(uuid4())
config = {"configurable": {"thread_id": thread_id}}
result = graph.invoke(initial_state, config=config)

while "__interrupt__" in result:
    payload = result["__interrupt__"][0].value
    print(payload["question"])
    answer = input("Your answer: ").strip()
    if not answer:
        print("Please provide an answer")
        continue
    result = graph.invoke(Command(resume=answer), config=config)
Important details:
1. Compile the graph with a checkpointer before using interrupts.
2. Reuse the same graph instance and same thread ID when resuming within the process.
3. The interrupted node starts executing again from its beginning on resume. Logging or other side effects before interrupt() may happen twice; keep those effects outside the node or make them idempotent.
4. A new thread ID starts a separate workflow. Treat thread IDs as session identifiers, not authentication.
5. Validate input in the CLI before sending a resume command. Invalid input inside a resumed node may raise an exception.
7. Checkpointing: what we use now
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
InMemorySaver supports pause/resume within the same running Python process. When the process exits, its checkpoints disappear. We intentionally deferred persistent SQLite/PostgreSQL checkpoints. For local interactive labs this is acceptable; for a deployed FastAPI application, it means restarting the server loses interview sessions. A single-process server is required for the initial in-memory prototype; multi-worker servers cannot reliably share this memory.
Later: persistent execution
A persistent checkpointer (SQLite for local development or PostgreSQL for a deployed app) stores execution state durably. This is different from business interview history, which might be modeled as tables for users, completed interviews, answers, scores, and reporting. Both can use PostgreSQL, but they serve different purposes.
8. How the final score is computed
def final_report_node(state: InterviewState) -> dict:
    evaluations = state["evaluations"]
    total = sum(item["evaluation"]["score"] for item in evaluations)
    average = total / len(evaluations) if evaluations else 0.0
    return {"average_score": average}
Example from one interview: scores 4, 0, 2, 2, 1; total = 9; average = 9 / 5 = 1.8. The earlier observed output of one evaluation and 1.0 average indicated a missing or incorrectly configured reducer. Verify the reducer fix before considering Lab 5.4 complete.
9. Debugging lessons from this project
ImportError: cannot import name 'human_answer_node'
The graph imported a function that had not yet been defined in app/graph/interview_nodes.py. Add the function at module scope and check its imports:
python -c "from app.graph.interview_nodes import human_answer_node; print('OK')"
python -c "from app.graph.interview_graph import build_interview_graph; build_interview_graph(); print('Graph OK')"
KeyError: 'average_score'
The graph reached END without visiting final_report_node. Ensure the finish branch of advance_question routes to final_report, and that final_report_node returns {"average_score": ...}.
Expected 5 evaluations, got 1
The graph evaluated all five answers but the state held only the last evaluation. Add Annotated[list[...], operator.add] to the evaluations field and return one-item lists from the evaluator.
Duplicate “Waiting for answer” log
The node printed before interrupt(). Resume restarts the node, so that print ran again. Put the display in the CLI, not before the interrupt.
ImportError for AnswerEvaluation
Ensure app/schemas/interview_schema.py actually defines the AnswerEvaluation Pydantic model imported by interview_service.py. Verify definitions and imports rather than guessing from a traceback.
10. Validation checklist
- [ ] human_answer_node imports successfully.
- [ ] build_interview_graph() compiles.
- [ ] Reducer unit test accumulates [4, 0, 2].
- [ ] Five questions are generated.
- [ ] Each question interrupts and accepts a candidate answer.
- [ ] Five evaluations are retained in the final state.
- [ ] Average score equals the arithmetic mean of the five evaluation scores.
- [ ] The graph terminates normally after question five.
- [ ] No API keys or local secrets are committed.
11. Git workflow — push without merging
Run from D:\ai-interview-assistant:
git status
git branch --show-current
If currently on main, create a feature branch before staging changes:
git switch -c feature/langgraph-workflow
If already on the feature branch, stay there. Copy this guide to docs/LANGGRAPH_README.md:
New-Item -ItemType Directory -Force docs
# Copy the downloaded LANGGRAPH_README.md into docs\LANGGRAPH_README.md
Stage only intended project files:
git add app/graph app/langgraph_interactive.py docs/LANGGRAPH_README.md
git diff --cached --stat
git diff --cached --check
git commit -m "feat: add interactive LangGraph interview workflow and learning guide"
git push -u origin feature/langgraph-workflow
If your actual branch has another name, replace feature/langgraph-workflow in the push command with that branch name. You may include other relevant modified project files after reviewing them. Do not run git merge, git switch main for a merge, or git push origin main. You can optionally open a draft pull request for review; a draft PR does not merge code.
12. What comes next
Milestone 6: FastAPI integration. Proposed endpoints:
- POST /interviews/start: create thread, invoke graph, return first interrupt payload.
- POST /interviews/{thread_id}/answer: resume with candidate answer, return next question or completion.
- GET /interviews/{thread_id}/state: inspect progress.
- GET /interviews/{thread_id}/report: fetch final score and evaluations.
Initially use one server process and InMemorySaver, with the explicit limitation that restarts lose sessions. Later introduce PostgreSQL-backed persistence and interview history, then RAG, authentication, and deployment.
Key takeaway: LangGraph gives you a stateful, resumable workflow around your LangChain services. Nodes do work; edges control flow; reducers merge state; interrupts hand control to a human; checkpoints let the workflow resume.# ai_learning