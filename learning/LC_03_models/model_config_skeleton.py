"""LC-03：可切换 chat model 配置手写骨架。

目标：
1. 把模型 provider、model name、base URL、API key 环境变量名集中管理。
2. 使用 `init_chat_model(...)` 创建 chat model。
3. 让 LC-02 的 agent 后续可以复用同一套模型配置思路。
"""

from __future__ import annotations  # 改变解释器处理类型注解的方式。让类型注解延迟求值

from dataclasses import dataclass   # 快速定义“只用来装数据的类”——DTO
from typing import Literal  # 类型标注工具——变量只能是某几个固定值

Provider = Literal["openai"]    # 只能是openai值

# 不用自己手写构造函数、字段赋值、基础展示方法——lombok Data。frozen——final不可变。
@dataclass(frozen=True)
class ModelSettings:
    """模型配置。
    你可以先只支持 OpenAI-compatible provider；后续再扩展 Anthropic、Google 等。
    """
    provider: Provider
    model: str      # 必传
    api_key_env: str
    base_url: str | None = None     # 可选，默认 None
    temperature: float = 0      # 可选，默认 0
    timeout: int = 30
    max_retries: int = 2


def load_model_settings() -> ModelSettings:
    """从环境变量读取模型配置。
    1. 用 `os.getenv(...)` 读取推荐环境变量。
    2. 给 provider、temperature、timeout、max_retries 设置合理默认值。
    3. 当必须的 model 或 API key 环境变量缺失时，给出清晰错误。
    """
    import os

    provider = os.getenv("MODEL_PROVIDER", "openai")       # DeepSeek 提供 OpenAI-compatible API
    model = os.getenv("MODEL_NAME", "deepseek-v4-flash")
    api_key_env = os.getenv("DEEPSEEK_API_KEY_ENV", "DEEPSEEK_API_KEY")     # 这里只是env，apikey在init_chat_model()里读
    base_url = os.getenv("MODEL_BASE_URL", "https://api.deepseek.com")

    if provider != "openai":
        raise ValueError(f"当前骨架只支持 openai provider，实际得到：{provider}")

    if not model:       # 是否为“空 / 假 / 没有有效值”
        raise ValueError("缺少环境变量 MODEL_NAME")

    ms = ModelSettings(
        provider=provider,
        model=model,
        api_key_env=api_key_env,
        base_url=base_url,
        temperature=0,
        timeout=30,
        max_retries=5,
    )
    return ms


def build_chat_model():
    """根据配置创建 chat model。
    TODO：
    1. 调用 `load_model_settings()`。
    2. 再从 `settings.api_key_env` 指向的环境变量读取真实 API key。
    3. 使用 `from langchain.chat_models import init_chat_model`。
    4. 把 model、model_provider、api_key、base_url、temperature 等参数传进去。
    """

    import os
    from langchain.chat_models import init_chat_model
    # from langchain.agents import create_agent   #上次用的是这个api

    model_setting = load_model_settings()

    api_key = os.getenv(model_setting.api_key_env)
    if not api_key:
        raise ValueError(f"缺少环境变量 {model_setting.api_key_env}")

    return init_chat_model(
        model=model_setting.model,
        model_provider=model_setting.provider,
        api_key=api_key,
        base_url=model_setting.base_url,
        temperature=model_setting.temperature,
        timeout=model_setting.timeout,
        max_retries=model_setting.max_retries,
    )


def main() -> None:
    """最小手动验证入口。
    1. 调用 `build_chat_model()`。
    2. 用 `model.invoke(...)` 问一个一句话问题。
    3. 打印返回消息的文本内容。
    """
    from dotenv import load_dotenv
    load_dotenv()   # 从 .env 文件加载环境变量，方便本地开发。

    model = build_chat_model()
    response = model.invoke("你好")
    for res in response:
        print( res)



if __name__ == "__main__":
    main()
