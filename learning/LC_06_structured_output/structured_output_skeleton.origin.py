"""LC-06：Structured Output 手写骨架。

目标：
1. 使用 Pydantic 定义结构化输出 schema。
2. 使用 create_agent(..., response_format=...) 让 agent 返回稳定结构。
3. 观察 result["structured_response"] 和普通 messages 的区别。
"""

from __future__ import annotations

from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field

from learning.LC_03_models.model_config_skeleton import build_chat_model


class TaskPlan(BaseModel):
    """A structured task plan extracted from a user request."""

    # TODO：补充任务标题字段，例如 title: str = Field(...)

    # TODO：补充优先级字段，建议使用 Literal["low", "medium", "high"]

    # TODO：补充步骤列表字段，建议使用 list[str]
    pass


class StudySummary(BaseModel):
    """A structured summary for one LangChain learning topic."""

    # TODO：补充 topic 字段，表示学习主题。

    # TODO：补充 key_points 字段，表示 3-5 条关键结论。

    # TODO：补充 next_action 字段，表示下一步建议。
    pass


def build_task_plan_agent():
    """创建返回 TaskPlan 结构的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[],
        # 提示：
        # 1. 直接传 TaskPlan 时，LangChain 会按模型能力自动选择结构化输出策略。
        # 2. 如果当前 provider 的原生结构化输出不稳定，可以改用 ToolStrategy(TaskPlan)。
        response_format=TaskPlan,
        system_prompt="你是一个简洁的任务规划助手。请只根据用户输入提炼结构化计划，不要编造不存在的信息。",
    )


def build_study_summary_agent():
    """创建返回 StudySummary 结构的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[],
        # TODO：把 response_format 补成 ToolStrategy(StudySummary)，观察工具策略的结构化输出。
        response_format=None,
        system_prompt="你是一个 LangChain 学习总结助手。请输出稳定、可复盘的结构化总结。",
    )


def inspect_structured_response(result: dict) -> None:
    """打印结构化结果和最终消息，便于对比观察。"""
    print("=== structured_response ===")
    # TODO：打印 result["structured_response"]，观察它是不是 Pydantic 对象。

    print("=== final message ===")
    # TODO：打印最后一条 message，可以使用 pretty_print()。

    print("=== dump ===")
    # TODO：如果 structured_response 是 Pydantic 对象，调用 model_dump() 转成 dict。


def main() -> None:
    """最小手动验证入口。"""
    _ = Literal
    _ = Field
    _ = ToolStrategy

    task_question = (
        "我明天想复习 LC-04 Messages 和 LC-05 Tools，"
        "时间只有 90 分钟，请帮我拆成一个高优先级学习计划。"
    )

    # TODO：创建 task plan agent，调用 invoke，并观察 structured_response。
    # agent = build_task_plan_agent()
    # result = agent.invoke({"messages": [{"role": "user", "content": task_question}]})
    # inspect_structured_response(result)

    summary_text = (
        "LC-06 学习 Structured Output。核心是 response_format、Pydantic schema、"
        "structured_response，以及 ProviderStrategy 和 ToolStrategy 的区别。"
    )

    # TODO：创建 study summary agent，用 summary_text 生成 StudySummary。
    _ = task_question
    _ = summary_text


if __name__ == "__main__":
    main()
