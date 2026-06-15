"""LC-05：Tools 工具调用手写骨架。

目标：
1. 使用 @tool 定义 search_notes 和 calculator 两个工具。
2. 使用 create_agent(...) 创建可以按需调用工具的 agent。
3. 可选观察 AIMessage.tool_calls，理解模型提出工具调用请求的结构。
"""

from __future__ import annotations

from langchain.agents import create_agent

from langchain.tools import tool    # 核心

from learning.LC_03_models.model_config_skeleton import build_chat_model

STUDY_NOTES = {
    "LC-03": "LC-03 学习了 chat model、provider、模型参数和 build_chat_model() 配置封装。",
    "LC-04": (
        "LC-04 学习了 SystemMessage、HumanMessage、AIMessage、ToolMessage "
        "和 message 字段观察。"
    ),      # 括号可省略，多行拼接，str类型，不是元组哈
}


@tool
def search_notes(query: str) -> str:
    """Search local LangChain study notes by keyword."""        # 除非有明确理由用中文，否则docstring用英文。英文兼容面更大（如provider、MCP、LangSmith）
    # 提示：
    # 1. 遍历 STUDY_NOTES。
    # 2. 如果 query 命中 key 或 value，就返回对应内容。
    # 3. 如果没有命中，返回“没有找到相关学习笔记：xxx”。
    if not query or not query.strip():
        return "无参数"

    normalized_query = query.strip().lower()

    for topic, note in STUDY_NOTES.items():
        normalized_topic = topic.lower()
        normalized_note = note.lower()

        if (
                normalized_query in normalized_topic
                or normalized_query in normalized_note
                or normalized_topic in normalized_query
        ):
            return f"{topic}: {note}"

    return f"没有找到相关学习笔记：{query}"


@tool
def calculator(expression: str) -> str:
    """Calculate a simple arithmetic expression."""
    # 提示：
    # 1. 先只支持数字、空格、+、-、*、/、括号。
    # 2. 不建议直接 eval 用户输入；可以先做字符白名单校验，再决定如何实现。
    # 3. 用 try/except 把错误转成可读字符串，例如“计算失败：...”。

    allowed_chars = set("0123456789+-*/() ")    # set(仅支持str)会把字符串拆成一个个字符，其他类型只能调 add

    if not expression:
        return "无参数"

    # 两种方法：1.正则。2.all、for、in、in
    #  all(Iterable)：遍历拼接&&   any()：遍历拼接||   in：contains()
    if not all(char in allowed_chars           for char in expression):   #  相当于 for char in expression 循环里面 判断 char in allowed_chars
        return f"计算失败：表达式包含不支持的字符。"

    import re   # 正则表达式模块
    if not re.match(r'^[\d\s+\-*/()]+$', expression):
        return f"计算失败：表达式包含不支持的字符。"

    try:
        return eval(expression)
    except Exception as e:
        return f"计算失败：{str(e)}"


# agent.invoke，自动调工具
def build_tools_agent():
    """创建带双工具的 agent。"""
    model = build_chat_model()
    return create_agent(
        model=model,
        tools=[search_notes, calculator],
        system_prompt="你是一个简洁的中文学习助手。需要查资料或计算时，请优先使用工具。",   # todo 这里的参数和SystemMessage的区别？
    )

# model.invoke，LLM说他想调工具
def inspect_tool_calls(question: str) -> None:
    """可选：只观察模型提出的工具调用请求，不自动执行工具。"""
    model = build_chat_model()
    model_with_tools = model.bind_tools([search_notes, calculator])
    response = model_with_tools.invoke(question)

    # print(response)
    print("=== 模型返回文本 ===")
    print(response.text)
    print("=== tool_calls ===")
    print(response.tool_calls)


def main() -> None:
    """最小手动验证入口。"""
    question = "请先查一下 LC-04 Messages 主要学了什么，再计算 18 * 7 + 6，并用两句话总结。"

    # 可选：先观察模型是否提出工具调用请求。
    inspect_tool_calls(question)

    agent = build_tools_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    print("=== agent result ===")
    print(result)


if __name__ == "__main__":
    main()

    # expression = "18 * 7 + 6啊"
    #
    # allowed_chars = set("0123456789+-*/() ")  # set(仅支持str)会把字符串拆成一个个字符，其他类型只能调 add
    #
    # # 两种方法：1.正则。2.all、for、in、in
    # #  all()：遍历拼接&&   any()：遍历拼接||   in：contains()
    # flag =all(char in allowed_chars for char in expression)
    # print(flag)
    #
    # import re  # 正则表达式模块
    #
    # flag2 = re.match(r'^[\d\s+\-*/()]+$', expression)
    # # 判断是否匹配成功
    # if flag2:
    #     print("表达式匹配成功")
    # else:
    #     print("表达式匹配失败")
