"""LC-15：本地学习资料 MCP server 手写骨架。

目标：
1. 使用 FastMCP 创建独立 server。
2. 暴露学习资料搜索与阶段摘要工具。
3. 通过 stdio transport 等待 MCP client 调用。

注意：
- stdio server 的 stdout 用于 MCP 协议通信，不要随意 print 调试信息。
- 本文件保留关键 TODO，建议学习者亲手补全。
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("langchain-study")

STUDY_NOTES: list[dict[str, str]] = [
    {
        "stage_id": "LC-05",
        "topic": "Tools",
        "summary": "工具让模型请求应用执行确定性函数；工具名、docstring 和参数 schema 会影响模型选择。",
    },
    {
        "stage_id": "LC-10",
        "topic": "Short-term Memory",
        "summary": "短期记忆由 checkpointer 按 thread_id 隔离，保存同一 thread 内的对话状态。",
    },
    {
        "stage_id": "LC-12",
        "topic": "Retrieval",
        "summary": "Retrieval 先把 query 映射到相关 Document，再把结果交给后续 RAG 或 agent。",
    },
    {
        "stage_id": "LC-14",
        "topic": "Agentic / Hybrid RAG",
        "summary": "Agentic RAG 让 agent 决定是否检索；Hybrid RAG 显式加入 query rewrite 和结果校验。",
    },
    {
        "stage_id": "LC-15",
        "topic": "MCP",
        "summary": "MCP 用统一协议连接 AI 应用与外部 tools、resources 和 prompts。",
    },
]


@mcp.tool()
def search_study_notes(query: str) -> dict[str, Any]:
    """按关键词搜索 LangChain 学习资料，返回匹配的阶段、主题和摘要。"""
    # 1：对 query 做 strip() 和 lower()。
    # 2：遍历 STUDY_NOTES，把 stage_id、topic、summary 合并后做不区分大小写匹配。
    # 3：返回 {"query": 原始查询, "matches": 匹配列表}。
    #
    # 可参考的核心写法（请理解后手写）：
    normalized_query = query.strip().lower()
    if not normalized_query:
        return {"query": query, "matches": []}
    matches = [
        note
        for note in STUDY_NOTES
        if normalized_query in " ".join(note.values()).lower()
    ]
    return {"query": query, "matches": matches}


@mcp.tool()
def get_stage_summary(stage_id: str) -> dict[str, Any]:
    """按 LC 阶段 ID 获取一条学习摘要，例如 LC-14。"""
    # 1：统一 stage_id 的空格与大小写。
    # 2：找到对应 note 后，返回 {"found": True, "note": note}。
    # 3：没有找到时返回 {"found": False, "stage_id": 标准化 ID}。
    normalized_stage_id = stage_id.strip().upper()
    for note in STUDY_NOTES:
        if note["stage_id"] == normalized_stage_id:
            return {"found": True, "note": note}
    return {"found": False, "stage_id": normalized_stage_id}


def main() -> None:
    """通过标准输入输出启动 MCP server。"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
