"""LC-18：LangGraph 入门手写骨架。

依次完成：纯 Python 直线图、Router 条件图、Model + Tool 循环。
关键 API 形状保留在注释中，建议理解后亲手输入。
"""

from __future__ import annotations

from operator import add # 把 +、- 等运算符包装成函数
from typing import Annotated, Literal # Annotated 给类型附加额外说明，比如更新 list 时，使用 add 函数

from langchain.tools import tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from learning.LC_13_two_step_rag.two_step_rag_skeleton import build_chat_model


# ============================================================================
# 练习一：纯 Python 直线图
# ============================================================================


# 纯 python 线性 state
class LinearState(TypedDict):
    raw_text: str # 原文本
    normalized_text: str # 标准化后的文本
    answer: str # 回答
    trace: Annotated[list[str], add] # 执行轨迹，reducer


def normalize_input(state: LinearState) -> dict:
    """清理输入，并记录节点执行轨迹。"""
    # 1：读取 raw_text，strip() 后返回 normalized_text。
    # trace 只返回 ["normalize_input"]，reducer 会负责累计。

    normalize_text = state["raw_text"].strip()
    return {"normalized_text": normalize_text, "trace": ["normalize_input"]} # 写入 state


def build_answer(state: LinearState) -> dict:
    """使用规范化文本生成固定教学回答。"""
    # 2：读取 normalized_text，返回 answer 和 ["build_answer"]。

    # 虽然这样原地修改传入的 state 然后 return 也可以，但是输入快照和节点更新混在一起，不利于 reducer 合并、并行执行和排错。
    # state["answer"] = f"答案是：{state['normalized_text']}"
    answer = f"答案是：{state['normalized_text']}"

    return {"answer":answer, "trace":["build_answer"]}

# 线性 Graph
def build_linear_graph():
    """构建 START -> normalize_input -> build_answer -> END。"""
    builder = StateGraph(LinearState)
    builder.add_node("normalize_input", normalize_input)
    builder.add_node("build_answer", build_answer)
    builder.add_edge(START, "normalize_input") # 普通 edge 表示固定顺序
    builder.add_edge("normalize_input", "build_answer") # 普通 edge 表示固定顺序
    builder.add_edge("build_answer", END) # 普通 edge 表示固定顺序
    return builder.compile()


def run_linear_demo() -> None:
    """调用直线图并打印最终 state。"""
    graph = build_linear_graph()

    # input 必须符合 state schema。 invoke 返回你定义的 state；
    # 而 agent 的 input 则是 消息状态 state schema，所以是 {"messages": [...]}
    result = graph.invoke({"raw_text": "  LangGraph  ", "trace": []})

    print(result) # state schema


# ============================================================================
# 练习二：Router 条件分支
# ============================================================================


class RouterState(TypedDict):
    request: str
    intent: Literal["question", "summary"] # 意图
    branch_result: str # 分支结果
    final_answer: str
    trace: Annotated[list[str], add] # reducer


# 分类 request
def classify_request(state: RouterState) -> dict:
    """用确定性规则识别 question 或 summary。"""
    # 5：request 以 "总结：" 开头时返回 summary，否则返回 question。
    intent = "summary" if state["request"].startswith("总结：") else "question"

    return {"intent": intent, "trace": ["classify_request"],}

# routing function，不是 Node！
def route_request(state: RouterState) -> Literal["question", "summary"]:
    """返回条件 edge 使用的路由标识。"""
    # 6：返回 state["intent"]。
    return state["intent"]


def answer_question(state: RouterState) -> dict:
    # 7：生成 question 分支的 branch_result，并记录 trace。
    return {"branch_result" : "回答问题", "trace": ["answer_question"]}


def summarize_text(state: RouterState) -> dict:
    # 8：生成 summary 分支的 branch_result，并记录 trace。
    return {"branch_result": "总结文本", "trace": ["summarize_text"]}


def finalize(state: RouterState) -> dict:
    # 9：根据 branch_result 生成 final_answer，并记录 trace。
    final_answer = f"处理完成：{state['branch_result']}"
    return {"final_answer": final_answer, "trace": ["finalize"]}


def build_router_graph():
    """构建条件分支和汇合点。"""
    # 10：添加 classify_request、两个分支和 finalize 节点。
    builder = StateGraph(RouterState)

    builder.add_node("classify_request", classify_request)
    builder.add_node("answer_question", answer_question)
    builder.add_node("summarize_text", summarize_text)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "classify_request")
    builder.add_conditional_edges(
        "classify_request",
        route_request,  # path
        {"question": "answer_question", "summary": "summarize_text"}, # intent 映射
    )
    # 两个分支都连接 finalize，finalize 再连接 END。
    builder.add_edge("answer_question", "finalize")
    builder.add_edge("summarize_text", "finalize")
    builder.add_edge("finalize", END)
    return builder.compile()


def run_router_demo() -> None:
    # 11：分别使用 question 和 summary 输入调用图并打印结果。
    graph = build_router_graph()
    question_result = graph.invoke({"request": "不总结：。问问题"})
    print("=== question ===")
    print(question_result)

    summary_result = graph.invoke({"request": "总结：xxx"})
    print("=== summary ===")
    print(summary_result)

# ============================================================================
# 练习三：Model + Tool 循环
# ============================================================================

# 继承 MessagesState（预定义 state），所以里面有 messages
class ModelToolState(MessagesState):
    request_id: str # 自定义扩展


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

    # 12：
    model_with_tools = model.bind_tools(tools) # create_agent(model=model, tools=tools) 会在内部完成工具绑定

    # 13：在函数内部定义 call_model(state: ModelToolState)：适配层
    def call_model(state: ModelToolState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]} # {"messages": [AIMessage]}

    # 14：
    builder = StateGraph(ModelToolState)
    builder.add_node("model", call_model) # # graph add_node 需要的是一个“接收 state、返回 state 更新”的节点，所以不能直接 model 作为节点
    builder.add_node("tools", ToolNode(tools)) # 专门的 ToolNode 节点读取最后一条 AI message 的 tool calls，执行对应工具，生成 ToolMessage 并写回 messages
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition) # 专门的 path：tools_condition，根据最后一条 AI message 决定，进入 call 和直接 End
    builder.add_edge("tools", "model") # 工具执行后必须回到 model，让模型读取 `ToolMessage` 并形成最终回答。
    return builder.compile()


def run_model_tool_demo() -> None:
    """观察普通回答与工具调用两条消息路径。"""
    cases = [
        {
            "request_id": "request-1",
            "question": "你好，请简单介绍一下你自己。", # HumanMessage -> AIMessage
        },
        {
            "request_id": "request-2",
            "question": "请调用工具查询 LC-18 的学习内容。", # HumanMessage -> AIMessage -> ToolMessage -> AIMessage
        },
    ]
    # 15：
    model = build_chat_model()
    graph = build_model_tool_graph(model)

    # 使用 {"messages": [("user", "...")], "request_id": "..."} 调用 graph。
    # 遍历 result["messages"]，观察 HumanMessage -> AIMessage ->
    # ToolMessage -> AIMessage（需要工具时）。
    for case in cases:
        result = graph.invoke({
            "messages": [("user", case["question"])],
            "request_id": case["request_id"],
        })

        print(f"\n=== {case['request_id']} ===")

        for message in result["messages"]:
            message.pretty_print()


def main() -> None:
    # 按学习进度一次只打开一个 demo。

    # 打印结果：{'raw_text': '  LangGraph  ', 'normalized_text': 'LangGraph', 'answer': '答案是：LangGraph', 'trace': ['normalize_input', 'build_answer']}
    # run_linear_demo()

    # 结果根据 request 中的 "总结：" 判断走哪个分支。
    # run_router_demo()

    # 结果就和正常的 agent loop：human-ai-tool-ai。结果也是 messages。
    run_model_tool_demo()


if __name__ == "__main__":
    main()
