"""LC-02：最小 LangChain agent 手写骨架。

目标：
1. 使用 `create_agent` 创建一个 agent。
2. 让 agent 能回答普通问题。
3. 让 agent 在需要时调用一个你自己写的 Python 工具函数。

运行前准备：
- 确认 `uv sync` 或等价方式已经安装 `langchain`。
- 按你选择的模型 provider 安装对应集成包并配置 API key。
"""

from langchain.agents import create_agent   # 核心

from learning.LC_03_models.model_config_skeleton import build_chat_model

# 原 LC-02 写法：
# import os
from langchain_openai import ChatOpenAI
# MODEL = "deepseek-v4-flash"
# MODEL = "openai:gpt-4.1-mini"


def get_weather(city: str) -> str:
    """返回指定城市的模拟天气。"""
    # 亲手补全这个工具函数。
    # 提示：可以先不用真实天气 API，直接根据 city 返回一段固定中文文本。
    # 例如：如果 city 是“北京”，返回“北京今天晴，适合散步。”
    # raise NotImplementedError("请先补全 get_weather 工具函数")
    if city == "北京":
        return "北京今天晴，适合散步"

    return f"{city}: 晴，适合继续学习 LangChain。"


def build_agent():
    """创建最小 agent。"""
    # 把 model 改成你当前可用的模型。
    # 官方 v1 写法支持直接传模型字符串，例如 "openai:gpt-5.4-mini"；
    # 也可以后续学习 LC-03 时再改成 `init_chat_model(...)`。
    # model = ChatOpenAI(
    #     model=MODEL,
    #     api_key=os.environ["DEEPSEEK_API_KEY"],
    #     base_url="https://api.deepseek.com",
    # )

    # 使用LC-03的模型配置骨架来创建模型实例
    model = build_chat_model()

    return create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="你是一个简洁、可靠的中文学习助手。",
    )


def main() -> None:
    agent = build_agent()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "北京今天适合跑步吗？"}]}
    )

    for message in result["messages"]:
        print(type(message).__name__)
        print(message.content)
        print("-" * 40)


if __name__ == "__main__":
    main()
