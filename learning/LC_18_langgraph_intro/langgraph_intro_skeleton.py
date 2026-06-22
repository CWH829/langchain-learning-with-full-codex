"""LC-18：LangGraph 入门手写骨架。

依次完成：纯 Python 直线图、Router 条件图、Model + Tool 循环。
关键 API 形状保留在注释中，建议理解后亲手输入。
"""

from __future__ import annotations

from operator import add
from typing import Annotated, Literal

from langchain.tools import tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from learning.LC_13_two_step_rag.two_step_rag_skeleton import build_chat_model


# ============================================================================
# 练习一：纯 Python 直线图
# ============================================================================


class LinearState(TypedDict):
    raw_text: str
    normalized_text: str
    answer: str
    trace: Annotated[list[str], add]


def normalize_input(state: LinearState) -> dict:
    """清理输入，并记录节点执行轨迹。"""
    # TODO 1：读取 raw_text，strip() 后返回 normalized_text。
    # trace 只返回 ["normalize_input"]，reducer 会负责累计。
    #
    # return {"normalized_text": ..., "trace": ["normalize_input"]}
    raise NotImplementedError


def build_answer(state: LinearState) -> dict:
    """使用规范化文本生成固定教学回答。"""
    # TODO 2：读取 normalized_text，返回 answer 和 ["build_answer"]。
    raise NotImplementedError


def build_linear_graph():
    """构建 START -> normalize_input -> build_answer -> END。"""
    # TODO 3：
    # builder = StateGraph(LinearState)
    # builder.add_node("normalize_input", normalize_input)
    # builder.add_node("build_answer", build_answer)
    # builder.add_edge(START, "normalize_input")
    # builder.add_edge("normalize_input", "build_answer")
    # builder.add_edge("build_answer", END)
    # return builder.compile()
    raise NotImplementedError


def run_linear_demo() -> None:
    """调用直线图并打印最终 state。"""
    # TODO 4：
    # graph = build_linear_graph()
    # result = graph.invoke({"raw_text": "  LangGraph  ", "trace": []})
    # print(result)
    raise NotImplementedError


# ============================================================================
# 练习二：Router 条件分支
# ============================================================================


class RouterState(TypedDict):
    request: str
    intent: Literal["question", "summary"]
    branch_result: str
    final_answer: str
    trace: Annotated[list[str], add]


def classify_request(state: RouterState) -> dict:
    """用确定性规则识别 question 或 summary。"""
    # TODO 5：request 以 "总结：" 开头时返回 summary，否则返回 question。
    # 同时记录 trace。
    raise NotImplementedError


def route_request(state: RouterState) -> Literal["question", "summary"]:
    """返回条件 edge 使用的路由标识。"""
    # TODO 6：返回 state["intent"]。
    raise NotImplementedError


def answer_question(state: RouterState) -> dict:
    # TODO 7：生成 question 分支的 branch_result，并记录 trace。
    raise NotImplementedError


def summarize_text(state: RouterState) -> dict:
    # TODO 8：生成 summary 分支的 branch_result，并记录 trace。
    raise NotImplementedError


def finalize(state: RouterState) -> dict:
    # TODO 9：根据 branch_result 生成 final_answer，并记录 trace。
    raise NotImplementedError


def build_router_graph():
    """构建条件分支和汇合点。"""
    # TODO 10：添加 classify_request、两个分支和 finalize 节点。
    # builder.add_conditional_edges(
    #     "classify_request",
    #     route_request,
    #     {"question": "answer_question", "summary": "summarize_text"},
    # )
    # 两个分支都连接 finalize，finalize 再连接 END。
    raise NotImplementedError


def run_router_demo() -> None:
    # TODO 11：分别使用 question 和 summary 输入调用图并打印结果。
    raise NotImplementedError


# ============================================================================
# 练习三：Model + Tool 循环
# ============================================================================


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
    """构建 model -> tools_condition -> ToolNode -> model 循环。"""
    tools = [lookup_learning_stage]

    # TODO 12：model_with_tools = model.bind_tools(tools)
    #
    # TODO 13：在函数内部定义 call_model(state: ModelToolState)：
    # response = model_with_tools.invoke(state["messages"])
    # return {"messages": [response]}
    #
    # TODO 14：
    # builder = StateGraph(ModelToolState)
    # builder.add_node("model", call_model)
    # builder.add_node("tools", ToolNode(tools))
    # builder.add_edge(START, "model")
    # builder.add_conditional_edges("model", tools_condition)
    # builder.add_edge("tools", "model")
    # return builder.compile()
    raise NotImplementedError


def run_model_tool_demo() -> None:
    """观察普通回答与工具调用两条消息路径。"""
    # TODO 15：
    # model = build_chat_model()
    # graph = build_model_tool_graph(model)
    # 使用 {"messages": [("user", "...")], "request_id": "..."} 调用 graph。
    # 遍历 result["messages"]，观察 HumanMessage -> AIMessage ->
    # ToolMessage -> AIMessage（需要工具时）。
    raise NotImplementedError


def main() -> None:
    # 按学习进度一次只打开一个 demo。
    # run_linear_demo()
    # run_router_demo()
    # run_model_tool_demo()
    pass


if __name__ == "__main__":
    main()
