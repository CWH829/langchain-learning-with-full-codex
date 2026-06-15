"""LC-05：Tools 工具调用手写骨架。

目标：
1. 使用 @tool 定义 search_notes 和 calculator 两个工具。
2. 使用 create_agent(...) 创建可以按需调用工具的 agent。
3. 可选观察 AIMessage.tool_calls，理解模型提出工具调用请求的结构。
"""

from __future__ import annotations

from langchain.agents import create_agent
from langchain.tools import tool

from learning.LC_03_models.model_config_skeleton import build_chat_model

STUDY_NOTES = {
    "LC-03": "LC-03 学习了 chat model、provider、模型参数和 build_chat_model() 配置封装。",
    "LC-04": (
        "LC-04 学习了 SystemMessage、HumanMessage、AIMessage、ToolMessage "
        "和 message 字段观察。"
    ),
}


@tool
def search_notes(query: str) -> str:
    """Search local LangChain study notes by keyword."""
    # TODO：请你亲手补全。
    # 提示：
    # 1. 遍历 STUDY_NOTES。
    # 2. 如果 query 命中 key 或 value，就返回对应内容。
    # 3. 如果没有命中，返回“没有找到相关学习笔记：xxx”。
    raise NotImplementedError("请先补全 search_notes 工具")


@tool
def calculator(expression: str) -> str:
    """Calculate a simple arithmetic expression."""
    # TODO：请你亲手补全。
    # 提示：
    # 1. 先只支持数字、空格、+、-、*、/、括号。
    # 2. 不建议直接 eval 用户输入；可以先做字符白名单校验，再决定如何实现。
    # 3. 用 try/except 把错误转成可读字符串，例如“计算失败：...”。
    raise NotImplementedError("请先补全 calculator 工具")


def build_tools_agent():
    """创建带双工具的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[search_notes, calculator],
        system_prompt="你是一个简洁的中文学习助手。需要查资料或计算时，请优先使用工具。",
    )


def inspect_tool_calls(question: str) -> None:
    """可选：只观察模型提出的工具调用请求，不自动执行工具。"""
    model = build_chat_model()
    model_with_tools = model.bind_tools([search_notes, calculator])
    response = model_with_tools.invoke(question)

    print("=== 模型返回文本 ===")
    print(response.text)
    print("=== tool_calls ===")
    print(response.tool_calls)


def main() -> None:
    """最小手动验证入口。"""
    question = "请先查一下 LC-04 Messages 主要学了什么，再计算 18 * 7 + 6，并用两句话总结。"

    # 可选：先观察模型是否提出工具调用请求。
    # inspect_tool_calls(question)

    agent = build_tools_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    print("=== agent result ===")
    print(result)


if __name__ == "__main__":
    main()
