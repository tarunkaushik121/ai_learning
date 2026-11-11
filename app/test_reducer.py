
from typing import Annotated, TypedDict
import operator

from langgraph.graph import StateGraph, START, END


class TestState(TypedDict):
    evaluations: Annotated[list[int], operator.add]


def first_node(state: TestState):
    return {"evaluations": [4]}


def second_node(state: TestState):
    return {"evaluations": [0]}


def third_node(state: TestState):
    return {"evaluations": [2]}


builder = StateGraph(TestState)

builder.add_node("first", first_node)
builder.add_node("second", second_node)
builder.add_node("third", third_node)

builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", "third")
builder.add_edge("third", END)

graph = builder.compile()

result = graph.invoke({"evaluations": []})

print("Evaluation history:", result["evaluations"])

assert result["evaluations"] == [4, 0, 2]

print("Reducer test passed!")
