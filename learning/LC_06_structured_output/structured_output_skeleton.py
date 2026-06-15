"""LC-06：Structured Output 手写骨架。

目标：
1. 使用 Pydantic 定义结构化输出 schema。
2. 使用 create_agent(..., response_format=...) 让 agent 返回稳定结构。
3. 观察 result["structured_response"] 和普通 messages 的区别。
"""

from __future__ import annotations

from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from pydantic import BaseModel, Field           # pydantic库：按规则解析、校验、生成对象

from learning.LC_03_models.model_config_skeleton import build_chat_model


# Schema —— 数据结构 规则 / 契约  / 模式。支持 Pydantic model、dataclass、TypedDict、JSON Schema
# 任务计划：标题、优先级、步骤
class TaskPlan(BaseModel):
    """A structured task plan extracted from a user request."""     #这里的 docstring 不是必须。重要的是字段约束 和 des。

    title: str = Field(..., description="任务标题，简洁明了地概括学习内容")     # ...：Ellipsis Python 中通用的内置对，在这里，表示 title 字段必填

    priority: Literal["low", "medium", "high"] = Field(description="任务优先级，必须是 low、medium 或 high")       # Pydantic v2 里不写默认值时，也是必填

    steps: list[str] = Field(min_length=1, description="任务步骤列表，每个步骤简洁明了，按执行顺序排列")        # min_length=1 确保 list[] 列表至少有一个步骤


# Schema
# 学习总结：主题、3-5条关键结论、下一步建议
class StudySummary(BaseModel):
    """A structured summary for one LangChain learning topic."""

    topic: str = Field(description="学习主题，简洁明了地概括总结内容")

    key_points: list[str] = Field(min_length=3, max_length=5, description="3-5 条关键结论，每个结论简洁明了")

    next_action: str = Field(description="下一步建议，指导用户如何继续学习")


def build_task_plan_agent():
    """创建返回 TaskPlan 结构的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[],
        # 提示：
        # 1. 直接传 TaskPlan 时，LangChain 会按模型能力自动选择结构化输出策略。
        # 2. 如果当前 provider 的原生结构化输出不稳定，可以改用 ToolStrategy(TaskPlan)。
        response_format=TaskPlan,       # 请求结构化输出
        system_prompt="你是一个简洁的任务规划助手。请只根据用户输入提炼结构化计划，不要编造不存在的信息。",
    )


def build_study_summary_agent():
    """创建返回 StudySummary 结构的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[],
        # 观察工具策略的结构化输出。
        response_format=ToolStrategy(StudySummary),     # 请求结构化输出
        # response_format=ProviderStrategy(StudySummary),     # 400： This response_format type is unavailable now。  ds不支持
        system_prompt="你是一个 LangChain 学习总结助手。请输出稳定、可复盘的结构化总结。",
    )


def inspect_structured_response(result: dict) -> None:
    """打印结构化结果和最终消息，便于对比观察。"""
    print("=== structured_response ===")
    # 打印 result["structured_response"]，观察它是不是 Pydantic 对象。
    print(result["structured_response"])             # key=value key=value key=value

    print("=== final message ===")
    # 打印最后一条 message，可以使用 pretty_print()。
    result["messages"][-1].pretty_print()            # Tool Message：TaskPlan / StudySummary



    print("=== dump ===")
    # 如果 structured_response 是 Pydantic —— BaseModel 对象，调用 model_dump() 转成 dict。
    if isinstance(result["structured_response"], BaseModel):
        print(result["structured_response"].model_dump())            # {key=value, key=value, key=value}
    else:
        print("structured_response 不是 BaseModel 对象，无法调用 model_dump()。")



def main() -> None:
    """最小手动验证入口。"""
    _ = Literal         # _ ：占位符，避免未使用导入的类型导致 linter
    _ = Field
    _ = ToolStrategy

    task_question = (
        "我明天想复习 LC-04 Messages 和 LC-05 Tools，"
        "时间只有 90 分钟，请帮我拆成一个高优先级学习计划。"
    )

    # 创建 task plan agent，调用 invoke，并观察 structured_response。
    agent = build_task_plan_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": task_question}]})

    # inspect_structured_response(result)

    summary_text = (
        "LC-06 学习 Structured Output。核心是 response_format、Pydantic schema、"
        "structured_response，以及 ProviderStrategy 和 ToolStrategy 的区别。"
    )


    # 创建 study summary agent，用 summary_text 生成 StudySummary。
    agent2 = build_study_summary_agent()
    result2 = agent2.invoke({"messages": [{"role": "user", "content": summary_text}]})

    inspect_structured_response(result2)


if __name__ == "__main__":
    main()
