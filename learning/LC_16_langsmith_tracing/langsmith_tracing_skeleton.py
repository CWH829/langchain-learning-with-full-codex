"""LC-16：LangSmith Tracing 手写骨架。

目标：
1. 通过环境变量自动追踪一次 tool agent 调用。
2. 使用 RunnableConfig 添加 run_name、tags 和 metadata。
3. 使用 @traceable 为普通 Python 函数手动埋点。
4. 观察自动 tracing 与手动埋点形成的 run tree。

说明：
- 请先由学习者手动在本地 .env 中配置 LangSmith。
- 不要在代码中硬编码或打印 LANGSMITH_API_KEY。
- 本文件保留关键 TODO，建议学习者亲手补全。
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_core.tracers.langchain import wait_for_all_tracers
from langsmith import traceable

from learning.LC_13_two_step_rag.two_step_rag_skeleton import build_chat_model


STAGE_NOTES = {
    "LC-15": (
        "LC-15 学习 MCP。实践完成了本地 FastMCP stdio server、"
        "MultiServerMCPClient、LangChain tools 转换和异步 agent 调用。"
    ),
    "LC-16": (
        "LC-16 学习 LangSmith Tracing。目标是观察 agent、model、tool 的调用树，"
        "并练习自动 tracing、RunnableConfig 和 @traceable 手动埋点。"
    ),
}


def check_langsmith_config() -> None:
    """检查必要配置，但绝不打印 API Key。"""
    load_dotenv()

    if not os.getenv("LANGSMITH_API_KEY"):
        raise ValueError("缺少环境变量 LANGSMITH_API_KEY，请先在本地 .env 中手动配置")

    if os.getenv("LANGSMITH_TRACING", "").lower() != "true":
        print("提示：LANGSMITH_TRACING 当前不是 true，自动 tracing 可能不会启用。")

    project = os.getenv("LANGSMITH_PROJECT", "default")
    print(f"LangSmith project: {project}")


@tool
def lookup_stage_note(stage_id: str) -> str:
    """按阶段 ID 查询学习笔记摘要，例如 LC-15。"""
    normalized_id = stage_id.strip().upper()
    return STAGE_NOTES.get(normalized_id, f"未找到阶段：{normalized_id}")


def build_agent():
    """构造用于观察 model -> tool -> model 调用链的 agent。"""
    # TODO 1：调用 build_chat_model() 创建模型。
    # TODO 2：调用 create_agent(...) 创建 agent。
    # TODO 3：tools 只传入 lookup_stage_note。
    # TODO 4：system_prompt 要求回答阶段问题前必须先调用工具。
    #
    # 可参考的核心结构（请理解后手写）：
    # return create_agent(
    #     model=model,
    #     tools=[lookup_stage_note],
    #     system_prompt="你是学习助手。回答阶段问题前必须先调用工具查询。",
    # )
    raise NotImplementedError("请补全 build_agent()")


def run_agent_trace() -> None:
    """自动追踪一次完整的 agent 调用。"""
    agent = build_agent()

    # TODO 1：准备 config 字典。
    # TODO 2：run_name 使用 "lc16-agent-trace"。
    # TODO 3：tags 至少包含 "lc-16" 和 "automatic-tracing"。
    # TODO 4：metadata 至少包含 stage="LC-16"、practice="agent"。
    # TODO 5：调用 agent.invoke({"messages": [...]}, config=config)。
    # TODO 6：打印最终一条 message 的 text。
    #
    # 建议问题：
    # "请查询阶段笔记，说明 LC-15 学习了什么。必须先调用工具。"
    #
    # RunnableConfig 参考结构：
    # {
    #     "run_name": "lc16-agent-trace",
    #     "tags": ["lc-16", "automatic-tracing"],
    #     "metadata": {
    #         "stage": "LC-16",
    #         "practice": "agent",
    #         "environment": "local",
    #     },
    # }
    raise NotImplementedError("请补全 run_agent_trace()")


# TODO 1：使用 @traceable(...) 装饰 load_study_context。
# TODO 2：name 使用 "load-study-context"。
# TODO 3：run_type 使用 "retriever"。
# TODO 4：添加能够区分 LC-16 手动埋点练习的 tags / metadata。
#
# 参考形式（请理解后手写，不要重复添加两个装饰器）：
# @traceable(
#     name="load-study-context",
#     run_type="retriever",
#     tags=["lc-16", "manual-tracing"],
#     metadata={"stage": "LC-16", "step": "load-context"},
# )
def load_study_context(stage_id: str) -> str:
    """模拟普通 Python 资料加载函数。"""
    normalized_id = stage_id.strip().upper()
    return STAGE_NOTES.get(normalized_id, f"未找到阶段：{normalized_id}")


# TODO 1：使用 @traceable(...) 装饰 answer_with_manual_trace。
# TODO 2：name 使用 "answer-with-manual-trace"。
# TODO 3：添加 tags 和 metadata。
#
# 外层 traceable run 应包含：
# - load_study_context() 产生的 child run。
# - model.invoke(...) 产生的 LangChain child run。
def answer_with_manual_trace(question: str, stage_id: str) -> str:
    """手动埋点的问答 pipeline。"""
    # TODO 1：调用 load_study_context(stage_id)。
    # TODO 2：调用 build_chat_model()。
    # TODO 3：构造 SystemMessage 和 HumanMessage。
    # TODO 4：调用 model.invoke(...)，让模型只根据 context 回答。
    # TODO 5：返回 response.text。
    #
    # 消息参考结构：
    # [
    #     SystemMessage(content=f"请只根据以下阶段资料回答：\n\n{context}"),
    #     HumanMessage(content=question),
    # ]
    raise NotImplementedError("请补全 answer_with_manual_trace()")


def run_manual_trace() -> None:
    """执行 @traceable 手动埋点练习。"""
    # TODO 1：调用 answer_with_manual_trace(...)。
    # TODO 2：stage_id 使用 "LC-16"。
    # TODO 3：打印返回的 answer。
    #
    # 建议问题：
    # "请用一句话说明这个阶段的学习目标。"
    raise NotImplementedError("请补全 run_manual_trace()")


def main() -> None:
    """依次执行自动 tracing 与手动埋点练习。"""
    check_langsmith_config()

    try:
        # TODO 1：调用 run_agent_trace()。
        # TODO 2：调用 run_manual_trace()。
        raise NotImplementedError("请补全 main() 中的两个实践入口")
    finally:
        # 短生命周期脚本退出前，等待后台 tracing 完成已产生 runs 的上报。
        wait_for_all_tracers()


if __name__ == "__main__":
    main()
