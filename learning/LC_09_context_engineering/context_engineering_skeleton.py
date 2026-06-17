"""LC-09：Context engineering 手写骨架。

本阶段重点：
1. dynamic prompt（动态提示词）：根据 runtime context 生成本次 system prompt。
2. tool context（工具上下文）：工具通过 ToolRuntime 读取 context/state。
3. model request override（模型请求覆盖）：用 request.override(...) 临时调整本次模型调用。
4. context lifecycle（上下文生命周期）：区分 transient（短暂）和 persistent（持久）。

说明：
- 代码实践仍以学习者手写为主。
- 每个关键 TODO 附近提供“核心 API”和注释掉的代码形状，供参考后手写。
- 本阶段只做轻量资料加载，不提前进入完整 RAG。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest, # 核心
    ModelResponse,
    dynamic_prompt,
    wrap_model_call,
) # 核心
from langchain.tools import ToolRuntime, tool

from learning.LC_03_models.model_config_skeleton import build_chat_model

STUDY_MATERIALS = {
    "LC-05": (
        "Tools 阶段重点是 @tool、参数 schema、tool_calls，"
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
        "Context engineering 阶段重点是 dynamic prompt、tool context、"
        "request.override(...) 和上下文成本控制。"
    ),
}

# content schema
@dataclass
class StudyContext:
    """本次 agent 调用的运行期上下文。"""
    user_id: str
    current_stage: str
    response_style: str = "concise"
    allow_advanced_tools: bool = False
    max_materials: int = 1

# 只取一部分资料
@tool
def load_study_material(topic: str, runtime: ToolRuntime[StudyContext]) -> str:
    """Load a small piece of LangChain study material by stage ID or keyword."""
    # 目标：
    # 1. 从 runtime.context 读取 StudyContext。
    # 2. 根据 topic 查询 STUDY_MATERIALS。
    # 3. 只返回最相关的少量资料，不一次性返回全部材料。
    # 4. 没有命中时，返回可查询阶段提示。
    context = runtime.context
    normalized_topic = topic.strip().lower()

    matched_items = []
    for stage_id, note in STUDY_MATERIALS.items():
        normalized_stage_id = stage_id.lower()
        normalized_note = note.lower()
        if (
                normalized_topic == normalized_stage_id
                or normalized_stage_id in normalized_topic
                or normalized_topic in normalized_note
        ):
            matched_items.append((stage_id, note))

    print(f"\n触发 load_study_material\n")

    if not matched_items:
        available_stages = "、".join(STUDY_MATERIALS.keys())
        return f"没有找到与“{topic}”相关的资料。可查询阶段：{available_stages}。"

    # max_materials 只限制“单次工具调用”的返回条数；
    # 如果模型多次调用工具，总返回资料仍可能超过 max_materials。
    selected_items = matched_items[: context.max_materials]  # 只取一部分

    lines = [f"{stage_id}: {note}" for stage_id, note in selected_items]
    return f"\n{lines}"


# 由 allow_advanced_tools 动态控制
@tool
def estimate_context_size(text: str) -> str:
    """Estimate context cost roughly by character count."""
    # 目标：
    # 1. 粗略估算文本进入上下文后的成本。
    # 2. 让你观察“上下文不是越多越好”。
    char_count = len(text.strip())
    estimated_tokens = char_count * 1

    print(f"\n触发 estimate_context_size\n")
    return (
        f"粗略估算：字符数 {char_count}，"
        f"约 {estimated_tokens} token。"
    )


@tool
def read_latest_user_message(runtime: ToolRuntime[StudyContext]) -> str:
    """Read the latest user message from agent state."""
    # 目标：
    # 1. 观察工具不仅能读 runtime.context，也能读 runtime.state。
    # 2. 从 runtime.state["messages"] 中找到最近一条用户消息。
    messages = runtime.state.get("messages", [])

    for message in reversed(messages):
        if getattr(message, "type", None) == "human":
            return f"读到最近一条用户消息：{message.content}"
    return "没有找到用户消息。"


# middleware-1（LC-08中没有介绍）：动态 system prompt 生成。
@dynamic_prompt
def build_study_prompt(request: ModelRequest) -> str:  # ModelRequest：模型调用前的请求对象。
    """根据 runtime context 动态生成本次 system prompt。"""
    # 目标：
    # 1. 从 request.runtime.context 读取 StudyContext。
    # 2. 根据 current_stage、response_style 生成简短 system prompt。
    # 3. 不把 STUDY_MATERIALS 全量拼进 prompt。
    # 4. 根据 len(request.messages) 处理长对话提示。
    context = request.runtime.context
    prompt_parts = [
        "你是 LangChain 学习助手。",
        f"当前学习阶段：{context.current_stage}。",
        f"回答风格：{context.response_style}。",
        "需要学习资料时，优先调用 load_study_material 按需查询。",
        "不要把全部 STUDY_MATERIALS 一次性塞进回答。",
        "再读一下最近一条的用户消息"
    ]

    if len(request.messages) >= 6:
        prompt_parts.append("当前消息较多，请回答更简洁，优先保留关键结论。")

    print("\n=== build_study_prompt 中间件生效 ===\n")

    return f"\n{prompt_parts}" # 动态 system prompt 属于 model request（模型请求）的临时上下文，是 transient（短暂的）。


# middleware-2：包住模型调用（调用前执行）
@wrap_model_call
def configure_model_context(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],  # handler(new_request)：继续执行模型调用。
) -> ModelResponse:
    """在模型调用前临时调整本次 model context。"""
    # 目标：
    # 1. 根据 StudyContext.allow_advanced_tools 筛选本次模型可见工具。
    # 2. 使用 request.override(...) 生成新的 ModelRequest。
    # 3. 调用 handler(new_request) 继续模型调用。
    # 4. 观察 request.override(...) 是 transient（短暂）调整。
    context = request.runtime.context
    tools = request.tools
    print("=== 当前 system_message ===")
    print(request.system_message) # 看一下动态 system prompt 是否生效

    allowed_tool_names = {"load_study_material", "read_latest_user_message"}
    if context.allow_advanced_tools:
        allowed_tool_names.add("estimate_context_size")

    filtered_tools = [
        current_tool
        for current_tool in tools if getattr(current_tool, "name", None) in allowed_tool_names
    ]  # 列表推导式
    print(f"\nconfigure_model_context 中间件生效，当前工具：{', '.join([tool.name for tool in tools])}，调整过滤后工具：{allowed_tool_names}\n")
    new_request = request.override(tools=filtered_tools)
    return handler(new_request)


def build_and_invoke_context_engineering_agent():
    """创建用于观察上下文工程的 agent。"""
    # 目标：
    # 1. 复用 LC-03 的 build_chat_model()。
    # 2. 给 agent 注册本阶段工具。
    # 3. 给 agent 注册 dynamic prompt 和 wrap_model_call middleware。
    # 4. 使用 context_schema=StudyContext 声明运行期上下文类型。
    model = build_chat_model()
    agent = create_agent(
        model=model,
        tools=[
            load_study_material,  # 只取小部分内容
            estimate_context_size,  # 计算tokne数
            read_latest_user_message,  # 读取最新用户消息
        ],
        middleware=[build_study_prompt, configure_model_context],  # 中间件，一个增加动态提示词、一个调整工具调用
        context_schema=StudyContext,  # 静态运行期上下文schema结构，结合invoke中context=context使用
    )

    """调用 agent，观察 context 如何影响行为。"""
    # 目标：
    # 1. 构造 StudyContext。
    # 2. 通过 agent.invoke(..., context=context) 传入运行期上下文。
    # 3. 通过 allow_advanced_tools 对比工具可见性变化。

    context = StudyContext(
        user_id="user-lc",
        current_stage="LC-09",
        response_style="concise",  # 简洁的
        allow_advanced_tools=False,
        max_materials=2,
    )
    question = (
        "请按需查找 LC-07、LC-08、LC-09 的资料，"
        "用三句话说明上下文工程和前两个阶段的关系。"
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        context=context,
    )

    """打印 messages，观察 prompt、工具调用和最终回答。"""
    print("=== result keys ===")
    print(result.keys())

    print("=== messages ===")
    for index, message in enumerate(result.get("messages", []), start=1):
        print(f"\n--- message {index}: {type(message).__name__} ---")
        message.pretty_print()


def main() -> None:
    """最小手动验证入口。"""
    build_and_invoke_context_engineering_agent()


if __name__ == "__main__":
    main()
