# LC-08：Middleware

## 本阶段目标

这一阶段学习 LangChain agent 的中间件机制。学完后，你应该能回答这些问题：

1. middleware 在 agent loop 里控制什么？
2. node-style hooks 和 wrap-style hooks 有什么区别？
3. 为什么日志、动态 prompt、工具过滤、重试、HITL、摘要都适合放到 middleware？
4. `HumanInTheLoopMiddleware` 为什么需要 checkpointer 和 `thread_id`？
5. `SummarizationMiddleware` 解决的是哪类上下文变长问题？

## 官方资料核对

已核对官方文档和本地锁定依赖：

- Middleware overview：<https://docs.langchain.com/oss/python/langchain/middleware/overview>
- Custom middleware：<https://docs.langchain.com/oss/python/langchain/middleware/custom>
- Prebuilt middleware：<https://docs.langchain.com/oss/python/langchain/middleware/built-in>
- Human-in-the-loop：<https://docs.langchain.com/oss/python/langchain/human-in-the-loop>
- 本项目当前锁定：`langchain==1.3.9`、`langgraph==1.2.5`

本地验证过这些导入和构造参数可用：

```python
from langchain.agents.middleware import (
    AgentMiddleware,
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
)
```

```text
HumanInTheLoopMiddleware(interrupt_on=...)
SummarizationMiddleware(model=..., trigger=..., keep=...)
```

关键结论：

- `create_agent(...)` 可以通过 `middleware=[...]` 接入一个或多个 middleware。
- middleware 不是单独的运行时；它运行在 `create_agent(...)` 编译出来的 LangGraph agent 内部。
- 自定义 middleware 可以用装饰器函数，也可以继承 `AgentMiddleware` 写类。
- hook 分两大类：node-style hooks 和 wrap-style hooks。
- HITL 会在工具执行前暂停，需要 checkpointer 保存可恢复状态。
- summarization 会在上下文变长时压缩历史消息，避免模型上下文持续膨胀。

## Middleware 解决什么问题

前面阶段主要写的是 agent 的“业务能力”：

- LC-05：给 agent 工具。
- LC-06：让 agent 返回结构化结果。
- LC-07：让工具读取 runtime context。

LC-08 开始关注 agent 的“控制逻辑”：

- 每次调用模型前后打日志。
- 按用户、权限或当前任务动态修改 system prompt。
- 只给模型暴露当前最相关的一部分工具。
- 对模型调用或工具调用做重试、fallback、限流。
- 对有副作用的工具加人工确认。
- 对过长对话做摘要，控制上下文长度。

这些逻辑的共同点是：它们不属于某一个工具本身，也不应该散落在每次 `invoke(...)` 前后。middleware 的价值就是把这些**横切逻辑**集中放在 agent loop 的固定位置。

## Agent loop 与 hooks

一个最简 agent loop 可以理解为：

```text
用户消息 -> 调模型 -> 模型决定是否调用工具 -> 执行工具 -> 再调模型 -> 最终回答
```

middleware 可以插在这个流程的不同位置。

### Node-style hooks

node-style hooks 在固定节点前后顺序执行，适合做日志、校验、轻量状态更新。

| hook | 触发时机 | 常见用途 |
| --- | --- | --- |
| `before_agent` | 每次 agent 调用开始前执行一次 | 初始化、请求日志 |
| `before_model` | 每次模型调用前执行 | 统计消息数、校验上下文 |
| `after_model` | 每次模型返回后执行 | 观察模型输出、拦截异常内容 |
| `after_agent` | 每次 agent 完成后执行一次 | 结果日志、清理 |

node-style hook 返回 `None` 表示不修改 state；返回 `dict` 表示把字段合并到 agent state 中。

### Wrap-style hooks

wrap-style hooks 包住某次模型调用或工具调用，适合做真正的控制流。

| hook | 触发时机 | 常见用途 |
| --- | --- | --- |
| `wrap_model_call` | 包住每次模型调用 | retry、fallback、动态模型、动态 prompt |
| `wrap_tool_call` | 包住每次工具调用 | 工具重试、工具输出清洗、工具审计 |

wrap-style hook 会拿到 `handler`。是否调用 `handler`、调用几次、调用前是否改 request、调用后是否改 response，都由 middleware 决定。

## 两种写法

### 装饰器写法

装饰器适合一个 hook 就能解决的小逻辑：

```python
from langchain.agents.middleware import before_model


@before_model
def log_before_model(state, runtime):
    print(f"即将调用模型，messages 数量：{len(state['messages'])}")
    return None
```

这里的 `@before_model` 是 Python 装饰器。可以先粗略理解为：把普通函数注册成 middleware hook。真正调用时机由 LangChain agent loop 决定，而不是你手动调用这个函数。

### 类写法

类写法适合同一个 middleware 里有多个 hook，或者需要初始化参数。

```python
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState


class StudyLoggingMiddleware(AgentMiddleware):
    def before_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        print(f"即将调用模型，messages 数量：{len(state['messages'])}")
        return None

    def after_model(self, state: AgentState, runtime) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        print(f"模型返回：{type(last_message).__name__}")
        return None
```

LC-08 的手写骨架使用类写法，因为它更适合同时观察 `before_agent`、`before_model`、`after_model`、`after_agent`。

## 执行顺序

多个 middleware 同时存在时，要注意顺序：

- `before_*` 按列表顺序执行。
- `after_*` 按列表反向执行。
- `wrap_*` 像函数嵌套一样，列表中靠前的 middleware 包住后面的 middleware。

示意：

```python
create_agent(
    model=model,
    tools=tools,
    middleware=[m1, m2, m3],
)
```

大致执行顺序：

```text
m1.before_model -> m2.before_model -> m3.before_model
m1.wrap_model_call(
    m2.wrap_model_call(
        m3.wrap_model_call(
            model
        )
    )
)
m3.after_model -> m2.after_model -> m1.after_model
```

所以顺序不是装饰品。越靠前的 middleware 越像外层控制器。

## HITL：Human-in-the-loop

HITL 用来在**高影响动作**执行前暂停 agent，让人决定是否批准。

典型场景：

- 发邮件、发通知、提交订单、删除数据。
- 写数据库、发布内容、调用真实外部系统。
- 任何“模型一旦执行就可能造成后果”的工具。

最小写法：

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    model=model,
    tools=[publish_study_summary],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"publish_study_summary": True}
        )
    ],
    checkpointer=InMemorySaver(),
)
```

调用时要带 `thread_id`：

```python
config = {"configurable": {"thread_id": "lc-08-hitl-demo"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "请发布学习总结"}]},
    config=config,
    version="v2",
)
```

如果模型决定调用 `publish_study_summary`，middleware 会在工具真正执行前产生 interrupt。之后可以用同一个 `config` 恢复：

```python
from langgraph.types import Command


agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config,
    version="v2",
)
```

`decisions `常见决策类型：

| 决策 | 含义 |
| --- | --- |
| `approve` | 批准，继续执行原工具调用 |
| `edit` | 修改工具名或参数后执行 |
| `reject` | 拒绝执行，并把反馈交还给 agent |
| `respond` | 用人工回复作为工具结果，适合“问用户”类工具 |

本阶段只需要先理解 `approve` 和 `reject`。`edit` 很强，但也更容易改变 agent 行为，练习时先保守使用。

## SummarizationMiddleware

agent 多轮调用时，消息、工具结果和中间步骤会越来越长。超过模型上下文窗口前，需要压缩历史。`SummarizationMiddleware` 的职责就是在触发条件满足时，把较早历史总结成更短的上下文。

最小写法：

```python
from langchain.agents.middleware import SummarizationMiddleware


agent = create_agent(
    model=model,
    tools=[search_study_notes],
    middleware=[
        SummarizationMiddleware(
            model=model,
            trigger=("messages", 8),
            keep=("messages", 4),
        )
    ],
)
```

可以先这样理解参数：

- `trigger=("messages", 8)`：当消息数量达到阈值时触发摘要。
- `keep=("messages", 4)`：摘要后保留最近 4 条消息。
- `model=model`：用哪个模型执行摘要任务。

LC-08 只做入门观察；更系统的上下文控制会放到 LC-09，线程内历史会放到 LC-10。

## Python 要点：装饰器

这一阶段会频繁看到 `@xxx`：

```python
@tool
def search_study_notes(query: str) -> str:
    ...
```

```python
@before_model
def log_before_model(state, runtime):
    ...
```

装饰器的本质是“把函数交给另一个函数处理，再把处理后的结果绑定回原名字”。粗略等价于：

```python
def search_study_notes(query: str) -> str:
    ...


search_study_notes = tool(search_study_notes)
```

对 LangChain 来说，装饰器常常用于注册额外元数据：

- `@tool`：把普通函数包装成模型可调用工具，并读取 docstring、参数类型生成 tool schema。
- `@before_model`：把普通函数注册成 middleware hook。

先不必深究装饰器闭包细节。当前最重要的是理解：装饰器会改变函数在框架眼中的身份。

## 本阶段手写实践任务

请亲手完成 `learning/LC_08_middleware/middleware_skeleton.py`：

1. 补全 `search_study_notes(...)`：
   - 参考 LC-05 的搜索工具。
   - 支持按阶段编号或正文关键词命中。
2. 补全 `publish_study_summary(...)`：
   - 先只返回模拟发布结果。
   - 不要真的写文件、发消息或调用外部系统。
3. 补全 `StudyLoggingMiddleware`：
   - 在 `before_agent`、`before_model`、`after_model`、`after_agent` 打印观察信息。
   - 先统一返回 `None`。
4. 补全 `build_logging_agent()`：
   - 创建 agent。
   - 接入 `StudyLoggingMiddleware()`。
   - 手动运行脚本，观察 hook 顺序。
5. 补全 `build_hitl_agent()`：
   - 接入 `HumanInTheLoopMiddleware(interrupt_on={"publish_study_summary": True})`。
   - 传入 `checkpointer=InMemorySaver()`。
6. 补全 `invoke_hitl_until_interrupt(...)`：
   - 使用固定 `thread_id` 触发一次发布请求。
   - 观察 `__interrupt__`。
   - 暂时不急着写 resume，先确认中断结构。
7. 选做 `build_summarization_agent()`：
   - 用较小的 `trigger=("messages", 8)` 方便观察。
   - 对比摘要前后 messages 的变化。

建议顺序：先 logging，再 HITL，最后 summarization。logging 能帮你看清 agent loop，HITL 和 summarization 才不容易像黑盒。

## 观察重点

- `before_agent` 和 `after_agent` 每次 `invoke` 只运行一次。
- `before_model` 和 `after_model` 可能运行多次，因为工具调用后 agent 通常还要再调一次模型生成最终回答。
- `after_model` 发生在模型提出 tool call 之后、工具执行之前，所以很适合观察即将发生的工具调用。
- HITL 拦截的是工具执行，不是拦截用户输入本身。
- 没有 checkpointer 时，HITL 无法可靠恢复暂停状态。
- `thread_id` 必须在中断和恢复时保持一致。
- summarization 是压缩上下文，不是长期记忆；摘要可能丢细节，所以关键事实仍要考虑更可靠的 memory/store。

## 常见坑

- 在 `middleware=[StudyLoggingMiddleware]` 里传类本身，而不是实例 `StudyLoggingMiddleware()`。
- 忘记把 middleware 传进 `create_agent(...)`，导致 hook 完全不执行。
- 在 hook 里返回了错误结构，例如返回字符串而不是 `dict | None`。
- 在 `after_model` 里直接假设最后一条消息一定有 `tool_calls`。
- HITL 忘记传 `checkpointer`。
- HITL 中断后 resume 换了新的 `thread_id`。
- 把 `publish_study_summary` 这类有副作用动作直接交给模型执行，没有人工确认或权限控制。
- 把 summarization 当成永久记忆。它只是压缩当前上下文，不适合保存长期用户偏好。

## 和后续阶段的关系

- LC-09 上下文工程：会继续研究如何用 middleware 动态控制 prompt、工具选择和上下文成本。
- LC-10 Short-term Memory：会系统学习 `thread_id`、checkpointer 和线程内消息历史。
- LC-11 Long-term Memory：会区分摘要、短期记忆和跨会话长期记忆。
- LC-16 LangSmith Tracing：会把手写 `print` 日志升级为可视化 trace 和运行观测。
