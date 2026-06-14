"""LC-03：可切换 chat model 配置手写骨架。

目标：
1. 把模型 provider、model name、base URL、API key 环境变量名集中管理。
2. 使用 `init_chat_model(...)` 创建 chat model。
3. 让 LC-02 的 agent 后续可以复用同一套模型配置思路。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Provider = Literal["openai"]


@dataclass(frozen=True)
class ModelSettings:
    """模型配置。

    TODO：你可以先只支持 OpenAI-compatible provider；后续再扩展 Anthropic、Google 等。
    """

    provider: Provider
    model: str
    api_key_env: str
    base_url: str | None = None
    temperature: float = 0
    timeout: int = 30
    max_retries: int = 2


def load_model_settings() -> ModelSettings:
    """从环境变量读取模型配置。

    TODO：
    1. 用 `os.getenv(...)` 读取推荐环境变量。
    2. 给 provider、temperature、timeout、max_retries 设置合理默认值。
    3. 当必须的 model 或 API key 环境变量缺失时，给出清晰错误。
    """
    raise NotImplementedError("请亲手补全 load_model_settings")


def build_chat_model():
    """根据配置创建 chat model。

    TODO：
    1. 调用 `load_model_settings()`。
    2. 再从 `settings.api_key_env` 指向的环境变量读取真实 API key。
    3. 使用 `from langchain.chat_models import init_chat_model`。
    4. 把 model、model_provider、api_key、base_url、temperature 等参数传进去。
    """
    raise NotImplementedError("请亲手补全 build_chat_model")


def main() -> None:
    """最小手动验证入口。

    TODO：
    1. 调用 `build_chat_model()`。
    2. 用 `model.invoke(...)` 问一个一句话问题。
    3. 打印返回消息的文本内容。
    """
    raise NotImplementedError("请亲手补全 main")


if __name__ == "__main__":
    main()
