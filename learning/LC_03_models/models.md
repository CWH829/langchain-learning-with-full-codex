# LC-03：Models

## 本阶段目标

这一阶段先把“模型对象”从 agent 里单独拎出来理解。学完后，你应该能回答三个问题：

1. LangChain v1 里 chat model 是什么，它和 agent 是什么关系？
2. 如何在不同 provider 之间切换，而不把业务代码写死到某一个厂商？
3. `temperature`、`max_tokens`、`timeout`、`max_retries`、`base_url` 这类参数分别控制什么？

## 官方资料核对

已核对 LangChain 官方文档：

- Models：`https://docs.langchain.com/oss/python/langchain/models`
- ChatOpenAI integration：`https://docs.langchain.com/oss/python/integrations/chat/openai`

关键结论：

- LangChain v1 推荐用 `from langchain.chat_models import init_chat_model` 初始化通用 chat model。
- 同一个标准 chat model 接口既可以独立调用，也可以传给 `create_agent`。
- provider 通常由独立集成包提供，例如当前仓库已经安装 `langchain-openai`。
- 模型名称会直接传给 provider API；很多新模型名不需要等待 LangChain 主包更新。
- 常见参数包括 `model`、`api_key`、`temperature`、`max_tokens`、`timeout`、`max_retries`。
- 使用 OpenAI-compatible 服务时，可以通过 `model_provider="openai"`、`base_url`、`api_key` 配置自定义地址。但 `ChatOpenAI` 的语义仍以官方 OpenAI API 规范为目标，第三方扩展字段不一定会保留。

## 核心概念

### chat model

chat model 是“能接收消息并返回消息”的模型接口。它不是 agent。

可以这样类比：

| Java / 后端概念 | LangChain 概念 |
| --- | --- |
| 一个可注入的 `Client` / `Service` | chat model 实例 |
| 调用远程 RPC / HTTP API | `model.invoke(...)` |
| 接口不变，替换实现类 | provider 切换 |
| 配置中心 / 环境变量 | model name、API key、base URL、参数 |

agent 会用 model 做推理和决策；model 本身只负责“根据输入消息生成输出消息”。LC-02 里 `create_agent(model=..., tools=...)` 的 `model` 参数，就是本阶段要单独理解的对象。

### provider

provider 是模型服务提供方，例如 OpenAI、Anthropic、Google、AWS Bedrock、OpenRouter，或兼容 OpenAI API 格式的服务。

在代码里要区分三层：

| 层次 | 示例 | 说明 |
| --- | --- | --- |
| 集成包 | `langchain-openai` | Python 依赖，提供模型类 |
| provider | `openai` | LangChain 用来选择集成实现 |
| model name | `gpt-5-nano`、`deepseek-v4-flash` | 传给 provider API 的具体模型 ID |

这和 Java 里“依赖 jar / SPI 实现 / 具体配置值”有点像：jar 负责能力接入，provider 负责路由到哪种实现，model name 是运行时参数。

## 常见参数

| 参数 | 作用 | 学习时建议 |
| --- | --- | --- |
| `model` | 具体模型名 | 放到环境变量或配置函数里，不要散落在业务代码中 |
| `model_provider` | 指定 provider | provider 无法从模型名推断时显式传入 |
| `api_key` | 认证凭据 | 优先从环境变量读取，不写进代码 |
| `base_url` | 自定义 API 地址 | OpenAI-compatible 服务常用 |
| `temperature` | 控制随机性 | 学习和测试阶段建议 `0` 或较低值 |
| `max_tokens` | 限制输出长度 | 避免模型一次生成过长 |
| `timeout` | 请求超时时间 | 网络不稳定时显式设置 |
| `max_retries` | 失败重试次数 | 速率限制或 5xx 会自动重试；401/404 这类配置错误不会靠重试解决 |

## 最小调用形态

官方通用入口的形态大致如下：

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-5-nano",
    temperature=0,
    timeout=30,
    max_retries=2,
)

response = model.invoke("用一句话解释 LangChain 的 chat model。")
print(response.text)
```

如果使用 OpenAI-compatible 服务，可以保留同一套思想：

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="openai",
    api_key="从环境变量读取",
    base_url="https://api.deepseek.com",
    temperature=0,
)
```

上面第二段是理解用片段，不建议直接把 key 字符串写入代码。

## 手写实践任务

本阶段代码实践不要急着写复杂 agent。先把 LC-02 里的模型创建逻辑抽出来。

建议你亲手完成：

1. 在 `learning/LC_03_models/model_config_skeleton.py` 中补全 `load_model_settings()`。
2. 从环境变量读取 provider、model、API key、base URL。
3. 用 `init_chat_model(...)` 创建模型。
4. 写一个最小 `main()`：调用模型回答一句中文问题。
5. 再把 LC-02 的 `hello_agent.py` 改成复用这个模型配置思路。

推荐环境变量名：

```bash
LANGCHAIN_MODEL_PROVIDER=openai
LANGCHAIN_MODEL_NAME=deepseek-v4-flash
LANGCHAIN_MODEL_BASE_URL=https://api.deepseek.com
LANGCHAIN_MODEL_API_KEY_ENV=DEEPSEEK_API_KEY
DEEPSEEK_API_KEY=你的 key
```

注意：这些配置建议你手动设置。环境变量、key、provider 参数是很有学习价值的排障入口，先自己走一遍会比直接让 Codex 写死更扎实。

## 常见坑

- `model_provider` 和 `model name` 不是一回事。`openai` 是 provider，`gpt-5-nano` 或 `deepseek-v4-flash` 才是模型名。
- `base_url` 写错时，可能出现 404、连接失败或 provider 返回格式异常。
- API key 环境变量名不统一。OpenAI 默认常见是 `OPENAI_API_KEY`，DeepSeek 示例里常用 `DEEPSEEK_API_KEY`。
- `temperature` 越高不代表越聪明，只是输出更发散；学习阶段低温更容易复现。
- 如果 401/404，优先检查 key、模型名、base URL，不要盲目增大 `max_retries`。

## 本阶段完成标准

- 能解释 chat model、provider、model name 的区别。
- 能把模型参数集中到一个配置函数中。
- 能用不同环境变量切换模型，而不改主要业务逻辑。
- 能说清楚 `temperature`、`timeout`、`max_retries` 的基本作用。

## 实践复盘

2026-06-14：

本阶段已经完成从“agent 里直接 new 一个模型对象”到“单独封装模型配置”的转变。你补全后的 `model_config_skeleton.py` 做到了几件关键事情：

1. 用 `ModelSettings` 集中承载模型配置，包括 provider、model name、API key 环境变量名、base URL、temperature、timeout、max retries。
2. 用 `@dataclass(frozen=True)` 表达“配置对象创建后不应随意修改”，这很接近 Java 里的不可变配置 DTO / record。
3. 用 `Literal["openai"]` 明确当前阶段只支持 OpenAI-compatible 调用路径，后续扩展 provider 时有一个清晰入口。
4. 用 `load_model_settings()` 统一读取环境变量，把配置读取和模型创建分开。
5. 用 `build_chat_model()` 读取真实 API key，并通过 `init_chat_model(...)` 创建 LangChain chat model。
6. 用 `python-dotenv` 在本地开发时加载 `.env`，避免把真实 key 写入代码。
7. 已实际调用 DeepSeek 模型并得到响应，说明 provider、model、base URL、API key、依赖安装和网络调用链路都已经跑通。
8. LC-02 已通过 `import build_chat_model` 复用本阶段的模型创建方法，agent 不再需要在 `build_agent()` 中直接创建 `ChatOpenAI`。

这一步的意义不只是“能调用模型”，而是开始把模型当成一个可替换的运行时依赖。后面 LC-04 Messages、LC-05 Tools、LC-06 Structured Output 都可以复用这个模型创建思路。

## 本次关键理解

### DeepSeek 为什么写成 `model_provider="openai"`

DeepSeek 不是 OpenAI provider。这里的 `"openai"` 表示使用 LangChain 的 OpenAI 协议适配器；真正的请求地址由 `base_url="https://api.deepseek.com"` 决定。

也就是说：

| 配置 | 当前含义 |
| --- | --- |
| `model_provider="openai"` | 使用 OpenAI-compatible 请求/响应格式 |
| `base_url="https://api.deepseek.com"` | 请求发往 DeepSeek |
| `model="deepseek-v4-flash"` | DeepSeek 上的具体模型名 |
| `api_key=...` | 从本地环境变量读取 DeepSeek key |

### `api_key_env` 的价值

`api_key_env` 不是 API key 本身，而是“保存 API key 的环境变量名”。这种二段式读取有一个好处：代码只关心“去哪个变量里找 key”，真实密钥仍留在本地环境中。

```python
api_key_env = "DEEPSEEK_API_KEY"
api_key = os.getenv(api_key_env)
```

这比直接把 key 写进代码安全，也更接近真实项目里的配置习惯。

### `.env` 和系统环境变量的优先级

`load_dotenv()` 默认不会覆盖已经存在的系统环境变量。也就是说，如果系统里已经有 `MODEL_NAME`，`.env` 里的同名值通常不会覆盖它。

学习阶段这反而是好事：你可以观察“到底哪个配置生效了”。如果未来明确希望 `.env` 覆盖系统变量，可以再考虑 `load_dotenv(override=True)`。

## 值得补充的改进点

这些不是必须马上改的 bug，更像下一轮代码打磨清单：

1. 环境变量命名可以统一。笔记里推荐的是 `LANGCHAIN_MODEL_*`，当前代码使用的是 `MODEL_*` 和 `DEEPSEEK_API_KEY_ENV`。两种都能用，但长期建议统一成一个前缀，避免项目变大后撞名。
2. `response` 是 LangChain 返回的 `AIMessage`。如果只想打印模型文本，优先使用 `print(response.text)`；遍历 `response` 更容易让初学者误以为它是普通字符串或列表。
3. `build_chat_model()` 的 TODO 可以在阶段完成后清理成正式说明，避免未来读代码时误判“还没完成”。
4. `max_retries=5` 可以保留，但要知道它只适合网络波动、限流或临时服务错误；如果是 401、404、模型名错误、base URL 错误，重试次数再多也没用。
5. `base_url` 目前有默认值，适合 DeepSeek 实践；如果以后真的要切 OpenAI 官方 API，可能需要让它为空，或根据 provider 决定默认值。
6. `python-dotenv` 已加入依赖后，建议保留一份 `.env.example` 作为配置模板，但真实 `.env` 不要提交。

## 阶段结论

LC-03 的最小目标已经达成：你已经能把模型配置从 agent 示例中抽出来，使用环境变量管理 provider、模型名、base URL 和 API key，并通过 LangChain v1 的 `init_chat_model(...)` 成功调用模型。

下一阶段 LC-04 Messages 会继续沿用这个模型对象，重点从“怎么创建模型”转向“模型输入输出的消息结构是什么”。
