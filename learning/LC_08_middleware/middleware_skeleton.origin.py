"""LC-08：Middleware 手写骨架。

目标：
1. 使用自定义 middleware 观察 agent 生命周期。
2. 使用 HumanInTheLoopMiddleware 给高影响工具加人工确认。
3. 选做：使用 SummarizationMiddleware 观察长对话摘要。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- HITL 需要 checkpointer + thread_id，后续 LC-10 会系统学习 memory/checkpointer。
"""

from __future__ import annotations

from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
)
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from learning.LC_03_models.model_config_skeleton import build_chat_model

STUDY_NOTES = {
    "LC-05": "Tools 阶段重点是 @tool、参数 schema、tool_calls 和 agent 自动执行工具。",
    "LC-06": (
        "Structured Output 阶段重点是 response_format、Pydantic schema 和 "
        "structured_response。"
    ),
    "LC-07": "Runtime 阶段重点是 context_schema、ToolRuntime 和 runtime.context。",
    "LC-08": "Middleware 阶段重点是 hooks、控制逻辑、HITL 和 summarization。",
}


@tool
def search_study_notes(query: str) -> str:
    """Search local LangChain study notes by keyword."""
    # TODO：
    # 1. 参考 LC-05 的 search_notes。
    # 2. 支持 query 命中阶段编号或笔记正文。
    # 3. 没有命中时返回清晰中文提示。
    raise NotImplementedError("请手写 search_study_notes")


@tool
def publish_study_summary(summary: str) -> str:
    """Publish a study summary after human approval."""
    # TODO：
    # 1. 先不要真的写文件或发消息，只模拟“发布”这个有副作用的动作。
    # 2. 返回一段中文结果，例如“已发布学习总结：...”。
    # 3. 后面会用 HumanInTheLoopMiddleware 拦截这个工具。
    raise NotImplementedError("请手写 publish_study_summary")


class StudyLoggingMiddleware(AgentMiddleware):
    """观察 agent 生命周期的自定义 middleware。"""

    def before_agent(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # TODO：
        # 1. 打印 agent 即将开始。
        # 2. 观察 state["messages"] 当前有多少条消息。
        # 3. 返回 None，表示不修改 agent state。
        _ = state
        _ = runtime
        return None

    def before_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # TODO：
        # 1. 打印即将调用模型。
        # 2. 观察当前 messages 数量。
        # 3. 返回 None。
        _ = state
        _ = runtime
        return None

    def after_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # TODO：
        # 1. 打印模型调用结束。
        # 2. 观察最后一条消息类型、content、tool_calls。
        # 3. 返回 None。
        _ = state
        _ = runtime
        return None

    def after_agent(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # TODO：
        # 1. 打印 agent 执行结束。
        # 2. 观察最终消息。
        # 3. 返回 None。
        _ = state
        _ = runtime
        return None


def build_logging_agent():
    """创建带日志 middleware 的 agent。"""
    model = build_chat_model()

    # TODO：
    # 1. 调用 create_agent(...)。
    # 2. tools 传入 search_study_notes。
    # 3. middleware 传入 StudyLoggingMiddleware()。
    # 4. system_prompt 提醒 agent 需要学习资料时使用工具。
    _ = model
    _ = create_agent
    raise NotImplementedError("请手写 build_logging_agent")


def build_hitl_agent():
    """创建带人工确认 middleware 的 agent。"""
    model = build_chat_model()
    checkpointer = InMemorySaver()

    # TODO：
    # 1. 调用 create_agent(...)。
    # 2. tools 传入 search_study_notes 和 publish_study_summary。
    # 3. middleware 中加入：
    #    HumanInTheLoopMiddleware(interrupt_on={"publish_study_summary": True})
    # 4. checkpointer 传入 checkpointer。
    # 5. 调用时必须配合同一个 thread_id 才能 resume。
    _ = model
    _ = checkpointer
    _ = HumanInTheLoopMiddleware
    raise NotImplementedError("请手写 build_hitl_agent")


def build_summarization_agent():
    """选做：创建带摘要 middleware 的 agent。"""
    model = build_chat_model()

    # TODO：
    # 1. 调用 create_agent(...)。
    # 2. middleware 中加入 SummarizationMiddleware。
    # 3. 可先使用较小 trigger，例如 trigger=("messages", 8)。
    # 4. keep 可以设置为 ("messages", 4)，方便观察历史被压缩。
    _ = model
    _ = SummarizationMiddleware
    raise NotImplementedError("请手写 build_summarization_agent")


def invoke_logging_agent(question: str) -> dict:
    """手动观察 logging middleware 的最小入口。"""
    agent = build_logging_agent()
    return agent.invoke({"messages": [{"role": "user", "content": question}]})


def invoke_hitl_until_interrupt(question: str) -> tuple[dict, dict]:
    """触发 HITL 中断，返回 config 和第一次 invoke 的结果。"""
    agent = build_hitl_agent()
    config = {"configurable": {"thread_id": "lc-08-hitl-demo"}}

    # TODO：
    # 1. 用 agent.invoke(..., config=config, version="v2") 发起调用。
    # 2. 问题里要求 agent 发布学习总结，让模型选择 publish_study_summary。
    # 3. 观察 result 中是否有 "__interrupt__"。
    _ = agent
    _ = config
    _ = question
    raise NotImplementedError("请手写 invoke_hitl_until_interrupt")


def inspect_result(result: dict) -> None:
    """打印 messages，便于观察 middleware 和工具调用过程。"""
    print("=== result keys ===")
    print(result.keys())

    print("=== messages ===")
    for index, message in enumerate(result.get("messages", [])):
        print(f"\n--- message {index}: {type(message).__name__} ---")
        message.pretty_print()

    if "__interrupt__" in result:
        print("=== interrupt ===")
        print(result["__interrupt__"])


def main() -> None:
    """最小手动验证入口。"""
    question = "请查一下 LC-07 和 LC-08 的学习重点，并用两句话总结。"
    result = invoke_logging_agent(question)
    inspect_result(result)


if __name__ == "__main__":
    main()
