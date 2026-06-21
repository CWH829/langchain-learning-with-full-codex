"""LC-15：LangChain MCP agent 客户端手写骨架。

目标：
1. 使用 MultiServerMCPClient 连接本地 stdio server。
2. 把 MCP tools 转换为 LangChain tools。
3. 使用异步 agent 调用工具。
4. 观察 AIMessage、ToolMessage 与 structured content。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- server 由 client 以子进程方式启动，不需要先手动启动。
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from learning.LC_13_two_step_rag.two_step_rag_skeleton import build_chat_model

SERVER_PATH = Path(__file__).with_name("study_mcp_server_skeleton.py").resolve()


def build_mcp_client() -> MultiServerMCPClient:
    """构造连接本地学习资料 server 的 MCP client。"""
    # 1：构造 MultiServerMCPClient。
    # 2：server 名称使用 "study"。
    # 3：transport 使用 "stdio"。
    # 4：command 使用 sys.executable，args 传入 SERVER_PATH 字符串。
    #
    return MultiServerMCPClient(
        {
            "study": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(SERVER_PATH)],
            }
        }
    )


def print_tools(tools: list[Any]) -> None:
    """打印 adapter 转换后的 LangChain tool 信息。"""
    print("\n=== loaded MCP tools ===")
    for tool in tools:
        print(f"name: {tool.name}")
        print(f"description: {tool.description}")
        print(f"args_schema: {tool.args_schema}")


def print_message_flow(messages: list[Any]) -> None:
    """观察 agent 的工具调用、工具结果与最终回答。"""
    print("\n=== message flow ===")
    for index, message in enumerate(messages, start=1):
        print(f"\n[{index}] {type(message).__name__}")

        if isinstance(message, AIMessage):
            print(f"text: {message.text}")
            print(f"tool_calls: {message.tool_calls}")
        elif isinstance(message, ToolMessage):
            print(f"name: {message.name}")
            print(f"status: {message.status}")
            print(f"content: {message.content}")
            print(f"artifact: {message.artifact}")
        else:
            print(f"content: {message.content}")


async def run_demo() -> None:
    """加载 MCP tools，构造 agent，并完成一次异步问答。"""
    client = build_mcp_client()

    # 1：使用 await client.get_tools() 加载 tools。
    # 2：调用 print_tools(tools)。
    # 3：创建 chat model。
    # 4：使用 create_agent(model, tools, system_prompt=...) 创建 agent。
    # 5：使用 await agent.ainvoke(...) 提问。
    # 6：把 result["messages"] 交给 print_message_flow(...)。
    #
    # 建议问题：
    # "请查询学习资料，说明 LC-14 的两种 RAG 路径有什么区别。"
    #
    # 注意：
    # - get_tools() 和 ainvoke() 都是异步调用，需要 await。
    # - system prompt 应明确要求阶段事实优先调用学习资料工具。
    tools = await client.get_tools()
    print_tools(tools)
    model = build_chat_model()
    agent = create_agent(
        model,
        tools,
        system_prompt="你是 LangChain 学习助手。需要阶段事实时先使用工具，回答保持简洁。",
    )

    result = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="请查询学习资料，说明 LC-14 的两种 RAG 路径有什么区别。")
                # {
                #     "role": "user",
                #     "content": "请查询学习资料，说明 LC-14 的两种 RAG 路径有什么区别。",
                # }
            ]
        }
    )
    print_message_flow(result["messages"])


def main() -> None:
    """从同步脚本入口启动异步事件循环。"""
    # 使用 asyncio.run(...) 执行 run_demo()。
    asyncio.run(run_demo())  # 执行异步任务


if __name__ == "__main__":
    main()
