"""LC-18：LangGraph 入门初始骨架副本。"""

from __future__ import annotations

from operator import add
from typing import Annotated, Literal

from langchain.tools import tool
from langgraph.graph import MessagesState
from typing_extensions import TypedDict


class LinearState(TypedDict):
    raw_text: str
    normalized_text: str
    answer: str
    trace: Annotated[list[str], add]


def normalize_input(state: LinearState) -> dict:
    raise NotImplementedError


def build_answer(state: LinearState) -> dict:
    raise NotImplementedError


def build_linear_graph():
    raise NotImplementedError


def run_linear_demo() -> None:
    raise NotImplementedError


class RouterState(TypedDict):
    request: str
    intent: Literal["question", "summary"]
    branch_result: str
    final_answer: str
    trace: Annotated[list[str], add]


def classify_request(state: RouterState) -> dict:
    raise NotImplementedError


def route_request(state: RouterState) -> Literal["question", "summary"]:
    raise NotImplementedError


def answer_question(state: RouterState) -> dict:
    raise NotImplementedError


def summarize_text(state: RouterState) -> dict:
    raise NotImplementedError


def finalize(state: RouterState) -> dict:
    raise NotImplementedError


def build_router_graph():
    raise NotImplementedError


def run_router_demo() -> None:
    raise NotImplementedError


class ModelToolState(MessagesState):
    request_id: str


@tool
def lookup_learning_stage(stage_id: str) -> str:
    """根据阶段 ID 查询一条本地教学信息。"""
    stage_notes = {
        "LC-18": "LC-18 学习 LangGraph 的 state、node、edge、Router 和 model/tool 循环。",
        "LC-19": "LC-19 将学习 multi-agent、supervisor、handoff 和 subagent。",
    }
    return stage_notes.get(stage_id.upper(), f"未找到阶段：{stage_id}")


def build_model_tool_graph(model):
    raise NotImplementedError


def run_model_tool_demo() -> None:
    raise NotImplementedError


def main() -> None:
    pass


if __name__ == "__main__":
    main()
