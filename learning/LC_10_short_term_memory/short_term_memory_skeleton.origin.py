"""LC-10：Short-term Memory 手写骨架。

目标：
1. 使用 checkpointer 给 agent 开启线程内短期记忆。
2. 使用 thread_id 区分不同对话线程。
3. 观察同一 thread 多轮对话如何保留 messages，不同 thread 如何隔离。
4. 通过 get_state(...) 查看 checkpoint 中保存的 agent state。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- 本阶段使用 InMemorySaver 做本地学习；生产环境可换成数据库型 checkpointer。
"""

from __future__ import annotations

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from learning.LC_03_models.model_config_skeleton import build_chat_model

STAGE_FACTS = {
    "LC-07": "Runtime 阶段重点是 context_schema、ToolRuntime、runtime.context 和 runtime.state。",
    "LC-08": "Middleware 阶段重点是 hooks、HITL、summarization 和 checkpointer + thread_id。",
    "LC-09": "Context engineering 阶段重点是 prompt、tools、runtime context 和上下文生命周期。",
    "LC-10": "Short-term memory 阶段重点是 checkpointer、thread_id 和线程内 messages 状态。",
}


@tool
def lookup_stage_fact(stage_id: str) -> str:
    """Look up a short local fact about a LangChain learning stage."""
    # TODO：
    # 1. 标准化 stage_id，例如转成大写、去掉前后空格。
    # 2. 在 STAGE_FACTS 中查找对应阶段。
    # 3. 命中时返回中文说明；未命中时返回清晰提示。
    # 参考写法：
    # normalized = stage_id.strip().upper()
    # return STAGE_FACTS.get(normalized, f"没有找到 {stage_id} 的阶段记录。")
    raise NotImplementedError("请手写 lookup_stage_fact")


def build_memory_agent():
    """创建带 short-term memory 的 agent。

    关键点：
    - checkpointer 必须传给 create_agent(...)。
    - 后续 invoke 时还必须传入 thread_id，状态才知道保存到哪条 thread。
    """
    model = build_chat_model()

    # TODO：
    # 1. 创建 InMemorySaver()。
    # 2. 调用 create_agent(...)。
    # 3. tools 传入 lookup_stage_fact。
    # 4. system_prompt 提醒 agent：需要阶段事实时使用工具，回答保持简洁。
    # 5. checkpointer 传入刚创建的 checkpointer。
    # 参考写法：
    # checkpointer = InMemorySaver()
    # return create_agent(
    #     model=model,
    #     tools=[lookup_stage_fact],
    #     system_prompt="你是 LangChain 学习助手。需要阶段事实时先使用工具，回答保持简洁。",
    #     checkpointer=checkpointer,
    # )
    _ = model
    _ = InMemorySaver
    _ = create_agent
    raise NotImplementedError("请手写 build_memory_agent")


def run_memory_demo(agent) -> None:
    """串联 LC-10 的核心实践流程。

    这里故意把 question 构建、config 构建、invoke 执行、result 解析、
    state 查看放在同一个函数中，方便顺着一条执行链观察 short-term memory。
    """
    # === 1. 准备同一个 thread 的两轮问题 ===
    same_thread_id = "lc-10-same-thread"
    same_thread_config = {"configurable": {"thread_id": same_thread_id}}

    first_question = "我的名字是林小夏，正在学习 LC-10。请记住这件事。"
    second_question = "我叫什么？我正在学哪个阶段？"

    # TODO：
    # 1. 用 same_thread_config 调用第一轮 agent.invoke(...)。
    # 2. 再用同一个 same_thread_config 调用第二轮 agent.invoke(...)。
    # 3. 观察第二轮是否能记住第一轮里的名字和阶段。
    # 参考写法：
    # first_result = agent.invoke(
    #     {"messages": [{"role": "user", "content": first_question}]},
    #     same_thread_config,
    # )
    # second_result = agent.invoke(
    #     {"messages": [{"role": "user", "content": second_question}]},
    #     same_thread_config,
    # )

    # === 2. 准备另一个 thread，观察记忆隔离 ===
    isolated_thread_id = "lc-10-isolated-thread"
    isolated_thread_config = {"configurable": {"thread_id": isolated_thread_id}}
    isolated_question = "我叫什么？我正在学哪个阶段？"

    # TODO：
    # 1. 不在 isolated_thread_id 里告诉 agent 名字。
    # 2. 直接调用 agent.invoke(...)。
    # 3. 观察 agent 不应该知道 same_thread_id 里的名字。
    # 参考写法：
    # isolated_result = agent.invoke(
    #     {"messages": [{"role": "user", "content": isolated_question}]},
    #     isolated_thread_config,
    # )

    # === 3. 在同一个函数中解析 result，观察 messages ===
    # TODO：
    # 1. 依次打印 first_result、second_result、isolated_result。
    # 2. 打印 result.keys()。
    # 3. 遍历 result["messages"]，打印 message 类型和 pretty_print()。
    # 参考写法：
    # for title, result in [
    #     ("same thread first result", first_result),
    #     ("same thread second result", second_result),
    #     ("isolated thread result", isolated_result),
    # ]:
    #     print(f"\n=== {title} ===")
    #     print(result.keys())
    #     for index, message in enumerate(result.get("messages", []), start=1):
    #         print(f"\n--- message {index}: {type(message).__name__} ---")
    #         message.pretty_print()

    # === 4. 查看 checkpoint 中保存的 thread state ===
    # TODO：
    # 1. 分别调用 agent.get_state(same_thread_config) 和 agent.get_state(isolated_thread_config)。
    # 2. 打印 snapshot.values.keys()。
    # 3. 从 snapshot.values 中取出 messages。
    # 4. 对比两个 thread 的 messages 数量和内容差异。
    # 参考写法：
    # for title, config in [
    #     ("same thread state", same_thread_config),
    #     ("isolated thread state", isolated_thread_config),
    # ]:
    #     snapshot = agent.get_state(config)
    #     messages = snapshot.values.get("messages", [])
    #     print(f"\n=== {title} ===")
    #     print(snapshot.values.keys())
    #     print(f"messages count: {len(messages)}")
    #     for index, message in enumerate(messages, start=1):
    #         print(f"{index}. {type(message).__name__}: {message.content}")
    _ = (
        agent,
        first_question,
        second_question,
        isolated_question,
        same_thread_config,
        isolated_thread_config,
    )
    raise NotImplementedError("请手写 run_memory_demo")


def main() -> None:
    """最小手动验证入口。"""
    agent = build_memory_agent()
    run_memory_demo(agent)


if __name__ == "__main__":
    main()
