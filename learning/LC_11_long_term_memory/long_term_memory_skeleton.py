"""LC-11：Long-term Memory 手写骨架。

目标：
1. 使用 store 保存跨 thread 的长期记忆。
2. 使用 context_schema 注入 user_id，按用户隔离长期记忆。
3. 在工具中通过 runtime.store 读写用户偏好。
4. 对比同一 user_id 跨 thread 可读、不同 user_id 相互隔离。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- 本阶段使用 InMemoryStore 做本地学习；生产环境应换成数据库型 store。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing_extensions import TypedDict # 类似 LC-06 中的 Pydantic，但不强校验

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.store.memory import InMemoryStore

from learning.LC_03_models.model_config_skeleton import build_chat_model

# schema
@dataclass
class Context:
    """每次 agent 调用时注入的运行期上下文。"""
    user_id: str

# key。TypedDict：用于描述 dict 的预期字段
class UserPreference(TypedDict):
    """保存到长期记忆中的用户偏好结构。"""
    language: str
    tone: str
    topic: str

# namespace
def profile_namespace(user_id: str) -> tuple[str, ...]:
    """构造用户偏好 profile 的 namespace。"""
    # 1. 返回一个 tuple，用于隔离不同用户的长期记忆。
    # 2. 推荐结构：("users", user_id, "preferences")。
    # 参考写法：
    return ("users", user_id, "preferences")


# 存
@tool
def save_user_preference(preference: UserPreference, runtime: ToolRuntime[Context]) -> str:
    """Save the current user's long-term preference profile."""
    # 1. 确认 runtime.store 不是 None。保证 create_agent 时有初始化。
    # 2. 从 runtime.context.user_id 取得当前用户 ID。
    # 3. 调用 profile_namespace(...) 得到 namespace。
    # 4. 使用 runtime.store.put(namespace, "profile", dict(preference)) 保存。
    # 5. 返回简洁中文提示。
    assert runtime.store is not None # 断言：开发环境的判断抛异常简写。生产环境还是要写 if throw。
    namespace = profile_namespace(runtime.context.user_id)
    runtime.store.put(namespace, "profile", dict(preference)) # 这里的 preference 由 LLM 生成的。
    return "已保存用户偏好。"

# 取
@tool
def load_user_preference(runtime: ToolRuntime[Context]) -> str:
    """Load the current user's long-term preference profile."""
    # 1. 确认 runtime.store 不是 None。
    # 2. 根据 runtime.context.user_id 构造 namespace。
    # 3. 使用 runtime.store.get(namespace, "profile") 读取。
    # 4. 如果没有记录，返回“未找到用户偏好”之类的提示。
    # 5. 如果有记录，通过 item.value 读取实际 dict 并返回。
    assert runtime.store is not None # create_agent() 声明 store
    namespace = profile_namespace(runtime.context.user_id)
    item = runtime.store.get(namespace, "profile")
    if item is None:
        return "未找到用户偏好。"
    return f"用户偏好：{item.value}"


def build_long_term_memory_agent():
    """创建带 long-term memory store 的 agent。

    关键点：
    - store 传给 create_agent(...) 后，工具中才能通过 runtime.store 访问。
    - context_schema 告诉 LangChain runtime.context 的结构。
    """
    model = build_chat_model()

    # 1. 创建 InMemoryStore()。
    # 2. 调用 create_agent(...)。
    # 3. tools 传入 save_user_preference 和 load_user_preference。
    # 4. store 传入刚创建的 store。
    # 5. context_schema 传入 Context。
    # 6. 返回 agent 和 store，方便 demo 末尾直接观察底层数据。
    store = InMemoryStore()
    agent = create_agent(
        model=model,
        tools=[save_user_preference, load_user_preference],
        system_prompt=(
            "你是 LangChain 学习助手。用户要求保存或读取偏好时，"
            "必须使用工具。回答保持简洁。"
        ),
        store=store, # 长期记忆。短期记忆是 checkpointer 保存的 state["messages"]。
        context_schema=Context, # 运行期上下文结构 —— runtime.context
    )
    return agent, store


def run_long_term_memory_demo() -> None:
    """串联 LC-11 的核心实践流程。"""
    agent, store = build_long_term_memory_agent()

    # === 1. 同一个 user_id，在 thread A 中保存长期偏好 ===
    thread_a_config = {"configurable": {"thread_id": "lc-11-thread-a"}} # thread_id 是 checkpointer 识别 thread 的约定 key,（比如在HITL中识别），是短时记忆的核心索引
    user_context = Context(user_id="user-001")

    # 1. 调用 agent.invoke(...)。
    # 2. 传入 thread_a_config。
    # 3. 传入 context=user_context。
    # 参考写法：
    save_result = agent.invoke(
        {"messages": [{"role": "user", "content": "请记住我的长期偏好：我喜欢中文回答，语气简洁，当前主题是 LangChain memory。"}]},
        config=thread_a_config, # 运行时配置（agent运行时会自动读取里面的thread，比如HITL、checkpointer的短期记忆）
        context=user_context, # 运行时上下文（给 agent / tools / prompt 看的）
    )

    # === 2. 同一个 user_id，换 thread B 读取长期偏好 ===
    thread_b_config = {"configurable": {"thread_id": "lc-11-thread-b"}}
    load_question = "请读取我的长期偏好，并用一句话概括。"

    # 1. 使用 thread_b_config 调用 agent.invoke(...)。
    # 2. context 仍然传 user_context。
    # 3. 观察换 thread 后仍能读到同一 user_id 的 store 数据。
    load_result = agent.invoke(
        {"messages": [{"role": "user", "content": load_question}]},
        config=thread_b_config,
        context=user_context, # 同一个 user
    )

    # === 3. 换另一个 user_id，观察长期记忆隔离 ===
    other_user_context = Context(user_id="user-002")
    other_thread_config = {"configurable": {"thread_id": "lc-11-thread-c"}}

    # 1. 使用 other_user_context 调用 agent.invoke(...)。
    # 2. 观察 user-002 不应该读到 user-001 的偏好。
    other_user_result = agent.invoke(
        {"messages": [{"role": "user", "content": load_question}]},
        config=other_thread_config,
        context=other_user_context,
    )

    # === 4. 打印 result messages，观察工具调用和回答 ===
    # 1. 依次打印 save_result、load_result、other_user_result。
    # 2. 遍历 result["messages"]，打印消息类型和 pretty_print()。
    for title, result in [
        ("测试一：save preference", save_result),
        ("测试二：load preference from another thread", load_result),
        ("测试三：load preference from another user", other_user_result),
    ]:
        print(f"\n=== {title} ===")
        for index, message in enumerate(result.get("messages", []), start=0):
            print(f"\n--- message {index}: {type(message).__name__} ---")
            message.pretty_print()

    # === 5. 直接观察 store 底层数据 ===
    # 1. 调用 store.search(("users",), limit=20)。
    # 2. 打印 item.namespace、item.key、item.value。
    # 3. 对比 namespace 中的 user_id。
    print("\n=== raw store items ===")
    for item in store.search(("users",), limit=20):
        print(item.namespace, item.key, item.value)


def main() -> None:
    """最小手动验证入口。"""
    run_long_term_memory_demo()


if __name__ == "__main__":
    main()
