"""LC-04：Messages 流分析手写骨架。

目标：
1. 用 SystemMessage / HumanMessage 构造模型输入。
2. 调用 LC-03 已封装的 build_chat_model()。
3. 打印并观察模型返回的 AIMessage 结构。
"""

from __future__ import annotations

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage

from learning.LC_03_models.model_config_skeleton import build_chat_model


def build_messages() -> list[BaseMessage]:
    """构造本阶段要发送给模型的消息列表。

    请你亲手补全：
    1. 第一条使用 SystemMessage，约束模型用简洁中文回答。
    2. 第二条使用 HumanMessage，询问 message 和普通字符串 prompt 的区别。
    3. 返回消息列表，注意顺序。
    """
    raise NotImplementedError("请先补全 build_messages()")


def print_message(message: BaseMessage) -> None:
    """打印一条 message 的关键字段。

    请你亲手补全：
    1. 打印 type(message).__name__。
    2. 打印 message.content。
    3. 如果存在 text / content_blocks / usage_metadata，也打印出来。

    提示：
    - 不是每种 message 都有完全一样的字段。
    - 可以用 getattr(message, "字段名", None) 安全读取。
    """
    raise NotImplementedError("请先补全 print_message()")


def main() -> None:
    """最小手动验证入口。"""
    model = build_chat_model()
    messages = build_messages()

    print("=== 输入 messages ===")
    for message in messages:
        print_message(message)

    response: AIMessage = model.invoke(messages)

    print("=== 模型返回 AIMessage ===")
    print_message(response)


if __name__ == "__main__":
    main()
