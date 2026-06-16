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
)  # 核心
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
    # 1. 参考 LC-05 的 search_notes。
    # 2. 支持 query 命中阶段编号或笔记正文。
    # 3. 没有命中时返回清晰中文提示。
    if not query.strip():
        return "无参数"

    query = query.strip().lower()

    for topic, note in STUDY_NOTES.items():
        normalized_topic = topic.lower()
        normalized_note = note.lower()
        if (
                query in normalized_topic
                or query in normalized_note
                or normalized_topic in query  # "LC-05 Tools"，也要能命中 LC-05
        ):
            return f"找到了！{topic}: {note}"
    return f"没有找到相关学习笔记：{query}"


# 高影响工具
@tool
def publish_study_summary(summary: str) -> str:
    """Publish a study summary after human approval."""
    # 1. 先不要真的写文件或发消息，只模拟“发布”这个有副作用的动作。
    # 2. 返回一段中文结果，例如“已发布学习总结：...”。
    # 3. 后面会用 HumanInTheLoopMiddleware 拦截这个工具。
    return f"已发布学习总结：{summary}"


# 也可用装饰器写
class StudyLoggingMiddleware(AgentMiddleware):
    """观察 agent 生命周期的自定义 middleware。"""

    # 没有 @Override，但是重写
    def before_agent(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # 1. 打印 agent 即将开始。
        # 2. 观察 state["messages"] 当前有多少条消息。
        # 3. 返回 None，表示不修改 agent state。
        print(f"看看state结构：{state}")     # 就是一个HumanMessage
        print(f"再看看runtime结构：{runtime}")    # LC-07中提到的那些

        messages = state["messages"]
        print("Agent 即将开始执行！")
        print(f"当前消息数量：{len(messages)}")
        messages[-1].pretty_print()  # 只要是 Message 对象，都有 pretty_print()

        return None  # 表示：我只是观察，不修改 agent state。

    def before_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # 1. 打印即将调用模型。
        # 2. 观察当前 messages 数量。
        # 3. 返回 None。
        messages = state["messages"]
        print("即将调用模型！")
        print(f"当前消息数量：{len(messages)}")
        _ = runtime  # runtime 这阶段学习暂时不用
        return None

    def after_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # 1. 打印模型调用结束。
        # 2. 观察最后一条消息类型、content、tool_calls。
        # 3. 返回 None。
        messages = state["messages"]
        print("模型调用结束！")
        print(f"当前消息数量：{len(messages)}")
        last_msg = messages[-1]
        print("最后一条消息：")
        last_msg.pretty_print()
        print(f"最后一条消息的类型：{type(last_msg).__name__}")
        print(f"最后一条消息的内容：{last_msg.content}")
        tool_calls = getattr(last_msg, "tool_calls", "无tool_calls")
        print(f"最后一条消息的工具调用：{tool_calls}")  # HumanMessage 没有 tool_calls 字段。

        _ = runtime
        return None

    def after_agent(self, state: AgentState, runtime) -> dict[str, Any] | None:
        # 1. 打印 agent 执行结束。
        # 2. 观察最终消息。
        # 3. 返回 None。
        print("Agent 执行结束！")
        messages = state["messages"]
        print(f"当前消息数量：{len(messages)}")    # 5次
        final_msg = messages[-1]
        print("最终消息：")
        final_msg.pretty_print()

        _ = runtime
        return None


def build_logging_agent():
    """创建带日志 middleware 的 agent。"""
    model = build_chat_model()

    # 1. 调用 create_agent(...)。
    # 2. tools 传入 search_study_notes。
    # 3. middleware 传入 StudyLoggingMiddleware()。
    # 4. system_prompt 提醒 agent 需要学习资料时使用工具。
    return create_agent(
        model=model,
        tools=[search_study_notes],
        middleware=[StudyLoggingMiddleware()],
        system_prompt="你是一个智能学习助手，当需要学习资料时，请优先使用工具 。",
    )


def build_hitl_agent():
    """创建带人工确认 middleware 的 agent。"""
    model = build_chat_model()
    checkpointer = InMemorySaver()

    # 1. 调用 create_agent(...)。
    # 2. tools 传入 search_study_notes 和 publish_study_summary。
    # 3. middleware 中加入：HumanInTheLoopMiddleware(interrupt_on={"publish_study_summary": True})
    # 4. checkpointer 传入 checkpointer。
    # 5. 调用时必须配合同一个 thread_id 才能 resume。

    interrupt_dict = {"publish_study_summary": True}  # 值不一定是 Ture，还可以更高级

    return create_agent(
        model=model,
        tools=[search_study_notes, publish_study_summary],
        middleware=[HumanInTheLoopMiddleware(interrupt_on=interrupt_dict)],
        checkpointer=checkpointer,  # checkpointer：保存暂停状态
        system_prompt="你是一个智能学习助手，当需要学习资料时，请优先使用工具。",
    )


# 压缩上下文
def build_summarization_agent():
    """选做：创建带摘要 middleware 的 agent。"""
    model = build_chat_model()

    # 1. 调用 create_agent(...)。
    # 2. middleware 中加入 SummarizationMiddleware。
    # 3. 可先使用较小 trigger，例如 trigger=("messages", 8)。
    # 4. keep 可以设置为 ("messages", 4)，方便观察历史被压缩。
    return create_agent(
        model=model,
        tools=[],
        middleware=[SummarizationMiddleware(
            model=model,
            trigger=("messages", 8),
            keep=("messages", 4)
        )],
        system_prompt="你是一个智能学习助手。",
    )


def invoke_logging_agent(question: str) -> dict:
    """手动观察 logging middleware 的最小入口。"""
    agent = build_logging_agent()
    return agent.invoke({"messages": [{"role": "user", "content": question}]})


def invoke_hitl_until_interrupt(question: str) -> tuple[dict, dict]:
    """触发 HITL 中断，返回 config 和第一次 invoke 的结果。"""
    agent = build_hitl_agent()

    config = {"configurable": {"thread_id": "lc-08-hitl-demo"}}

    # 1. 用 agent.invoke(..., config=config, version="v2") 发起调用。
    # 2. 问题里要求 agent 发布学习总结，让模型选择 publish_study_summary。
    # 3. 观察 result 中是否有 "__interrupt__"。
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config,  # 重点
        version="v2",  # HITL 场景建议按官方示例带上它，result 用来获得新版 interrupt 结构
    )
    return config, result


def inspect_result(result: Any) -> None:
    """打印 messages，便于观察 middleware 和工具调用过程。"""

    # 如果是普通invoke，则是dict、如果是version=v2，则是GraphOutput对象
    if hasattr(result, "value") and hasattr(result, "interrupts"):
        output = result.value
        interrupts = result.interrupts
    else:
        output = result
        interrupts = ()

    print("=== result type ===")
    print(type(result).__name__)

    print("=== result keys ===")
    # 如果是dict
    if isinstance(output, dict):
        print(output.keys())
        messages = output.get("messages", [])
    else:
        # 如果是对象
        print(f"output 不是 dict：{type(output).__name__}")
        messages = getattr(output, "messages", [])

    print("=== messages ===")
    for index, message in enumerate(messages):
        print(f"\n--- message {index}: {type(message).__name__} ---")
        message.pretty_print()

    if interrupts:
        print("=== interrupts ===")
        print(interrupts)


def main() -> None:
    """最小手动验证入口。"""

    print("\n\n=== 测试 LOGGING 中间件 ===")
    normal_question = "请查一下 LC-07 和 LC-08 的学习重点"
    result = invoke_logging_agent(normal_question)
    inspect_result(result)

    print("\n\n=== 测试 HITL 中间件 ===")
    hitl_question = "请根据 LC-08 的学习重点，发布一段简短学习总结。"
    config, hitl_result = invoke_hitl_until_interrupt(hitl_question)
    print("=== hitl config ===")
    print(config)
    inspect_result(hitl_result)

    print("\n\n=== 测试 SUMMARY 上下文压缩 中间件 ===")
    # todo


if __name__ == "__main__":
    main()
