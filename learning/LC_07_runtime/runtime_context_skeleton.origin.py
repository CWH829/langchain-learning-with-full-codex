"""LC-07：Runtime context 手写骨架。

目标：
1. 使用 dataclass 定义 UserContext。
2. 使用 create_agent(..., context_schema=UserContext) 声明运行期上下文结构。
3. 在工具中通过 runtime: ToolRuntime[UserContext] 读取 runtime.context。
4. 可选观察 runtime.state 中的 messages。
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import ToolRuntime, tool

from learning.LC_03_models.model_config_skeleton import build_chat_model

LEARNING_PROFILES = {
    "user-lc": {
        "level": "LangChain 入门到主线推进中",
        "focus": "agent、tools、structured output、runtime context",
    },
    "user-review": {
        "level": "复习模式",
        "focus": "巩固 Messages、Tools 和 Structured Output",
    },
}


@dataclass
class UserContext:
    """本次 agent 调用的静态上下文。"""

    user_id: str
    user_name: str
    study_stage: str
    preferred_language: str = "zh"


@tool
def get_learning_profile(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's learning profile."""
    # TODO：
    # 1. 从 runtime.context 读取 user_id、user_name、study_stage。
    # 2. 用 user_id 查询 LEARNING_PROFILES。
    # 3. 返回一段中文说明，例如：
    #    “用户 Codex 学习者 当前处于 LC-07，重点是 ...”
    # 4. 如果没有查到 profile，返回“没有找到用户画像：xxx”。
    raise NotImplementedError("请手写：从 runtime.context 读取用户信息并返回学习画像。")


@tool
def get_recent_user_message(runtime: ToolRuntime[UserContext]) -> str:
    """Get the latest human message from runtime state."""
    # TODO：
    # 1. 从 runtime.state 中读取 messages。
    # 2. 从后往前找最后一条 HumanMessage。
    # 3. 返回它的 content。
    # 4. 如果没有找到，返回“没有找到用户消息”。
    #
    # 提示：
    # messages = runtime.state.get("messages", [])
    # for message in reversed(messages):
    #     if isinstance(message, HumanMessage):
    #         ...
    raise NotImplementedError("请手写：从 runtime.state 中读取最近一条用户消息。")


def build_runtime_agent():
    """创建能够读取 runtime context 的 agent。"""
    model = build_chat_model()

    # TODO：
    # 1. 调用 create_agent(...)。
    # 2. tools 传入 get_learning_profile 和 get_recent_user_message。
    # 3. context_schema 传入 UserContext。
    # 4. system_prompt 提醒 agent：需要用户画像或当前消息时优先使用工具。
    _ = (create_agent, model)
    raise NotImplementedError("请手写：创建带 context_schema 的 agent。")


def invoke_runtime_agent(question: str) -> dict:
    """用固定 UserContext 调用 agent，便于手动观察。"""
    agent = build_runtime_agent()

    context = UserContext(
        user_id="user-lc",
        user_name="Codex 学习者",
        study_stage="LC-07 Runtime",
    )

    # TODO：
    # 调用 agent.invoke(...)，把 question 放进 messages，并通过 context= 传入上面的 context。
    _ = (agent, question, context)
    raise NotImplementedError("请手写：调用 agent.invoke(..., context=context)。")


def inspect_result(result: dict) -> None:
    """打印最终消息和完整 messages，观察工具调用过程。"""
    print("=== final message ===")
    result["messages"][-1].pretty_print()

    print("=== all messages ===")
    for index, message in enumerate(result["messages"], start=1):
        print(f"\n--- message {index}: {type(message).__name__} ---")
        message.pretty_print()


def main() -> None:
    """最小手动验证入口。"""
    _ = HumanMessage

    question = (
        "请先查看我的学习画像，再结合我刚才这条消息，"
        "用两句话说明 LC-07 Runtime 应该重点理解什么。"
    )

    result = invoke_runtime_agent(question)
    inspect_result(result)


if __name__ == "__main__":
    main()
