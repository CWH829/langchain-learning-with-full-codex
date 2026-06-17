"""LC-09：Context engineering 手写骨架。

目标：
1. 使用动态 prompt 控制模型本次调用看到的指令。
2. 使用工具按需加载学习资料，而不是把所有资料塞进 system prompt。
3. 使用 runtime context 控制答复风格和工具可见性。
4. 观察 transient model context 与 persistent state/store 的边界。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- LC-09 只做轻量资料加载，不提前进入完整 RAG；LC-12 之后会系统学习 retrieval。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    dynamic_prompt,
    wrap_model_call,
)
from langchain.tools import ToolRuntime, tool

from learning.LC_03_models.model_config_skeleton import build_chat_model

STUDY_MATERIALS = {
    "LC-05": (
        "Tools 阶段重点是 @tool、参数 schema、tool_calls、"
        "以及 agent 如何自动执行模型请求的工具。"
    ),
    "LC-06": (
        "Structured Output 阶段重点是 response_format、Pydantic schema、"
        "structured_response 和 model_dump()。"
    ),
    "LC-07": (
        "Runtime 阶段重点是 context_schema、ToolRuntime、runtime.context "
        "和 runtime.state。"
    ),
    "LC-08": (
        "Middleware 阶段重点是 hooks、wrap_model_call、wrap_tool_call、"
        "HITL 和 SummarizationMiddleware。"
    ),
    "LC-09": (
        "Context engineering 阶段重点是 prompt、messages、tools、"
        "tool context、life-cycle context 和上下文成本控制。"
    ),
}


@dataclass
class StudyContext:
    """本次 agent 调用的静态上下文。"""

    user_id: str
    current_stage: str
    response_style: str = "concise"
    allow_advanced_tools: bool = False


@tool
def load_study_material(topic: str, runtime: ToolRuntime[StudyContext]) -> str:
    """Load a small piece of study material by stage ID or keyword."""
    # TODO：
    # 1. 从 runtime.context 读取 current_stage 和 response_style。
    # 2. 在 STUDY_MATERIALS 中查找 topic 命中的阶段编号或正文。
    # 3. 只返回最相关的少量资料，不要一次性返回全部材料。
    # 4. 没有命中时，返回清晰中文提示。
    _ = runtime
    raise NotImplementedError("请手写 load_study_material")


@tool
def estimate_context_size(text: str) -> str:
    """Estimate context size roughly by character count."""
    # TODO：
    # 1. 用 len(text) 估算字符数量。
    # 2. 用一个非常粗略的经验值估算 token，例如中文可先按 1 字符约 1 token 理解。
    # 3. 返回中文说明，帮助观察上下文成本。
    raise NotImplementedError("请手写 estimate_context_size")


@dynamic_prompt
def build_study_prompt(request: ModelRequest) -> str:
    """根据 runtime context 动态生成 system prompt。"""
    # TODO：
    # 1. 从 request.runtime.context 读取 StudyContext。
    # 2. 根据 current_stage、response_style 生成简短 system prompt。
    # 3. 不要把 STUDY_MATERIALS 全量拼进 prompt。
    # 4. 可以根据 len(request.messages) 对长对话加一句“回答更简洁”。
    _ = request
    raise NotImplementedError("请手写 build_study_prompt")


@wrap_model_call
def filter_tools_by_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """根据 runtime context 控制本次模型调用可见的工具。"""
    # TODO：
    # 1. 从 request.runtime.context 读取 allow_advanced_tools。
    # 2. 如果 allow_advanced_tools=False，只保留 load_study_material。
    # 3. 如果 allow_advanced_tools=True，可以保留 estimate_context_size。
    # 4. 使用 request.override(tools=filtered_tools) 生成新 request。
    # 5. 调用并返回 handler(request)。
    _ = request
    return handler(request)


def build_context_engineering_agent():
    """创建用于观察上下文工程的 agent。"""
    model = build_chat_model()

    # TODO：
    # 1. 调用 create_agent(...)。
    # 2. tools 传入 load_study_material 和 estimate_context_size。
    # 3. middleware 传入 build_study_prompt 和 filter_tools_by_context。
    # 4. context_schema 传入 StudyContext。
    _ = model
    _ = create_agent
    raise NotImplementedError("请手写 build_context_engineering_agent")


def invoke_context_engineering_agent(
    question: str,
    *,
    allow_advanced_tools: bool = False,
) -> dict:
    """用固定 StudyContext 调用 agent，便于手动观察。"""
    agent = build_context_engineering_agent()

    context = StudyContext(
        user_id="user-lc",
        current_stage="LC-09",
        response_style="concise",
        allow_advanced_tools=allow_advanced_tools,
    )

    # TODO：
    # 1. 调用 agent.invoke(...)。
    # 2. messages 中放入 question。
    # 3. 通过 context=context 传入运行期上下文。
    _ = (agent, question, context)
    raise NotImplementedError("请手写 invoke_context_engineering_agent")


def inspect_result(result: dict) -> None:
    """打印 messages，观察 prompt、工具调用和最终回答。"""
    print("=== result keys ===")
    print(result.keys())

    print("=== messages ===")
    for index, message in enumerate(result.get("messages", []), start=1):
        print(f"\n--- message {index}: {type(message).__name__} ---")
        message.pretty_print()


def main() -> None:
    """最小手动验证入口。"""
    question = (
        "请按需查找 LC-07、LC-08、LC-09 的资料，"
        "用三句话说明上下文工程和前两个阶段的关系。"
    )
    result = invoke_context_engineering_agent(question)
    inspect_result(result)


if __name__ == "__main__":
    main()

