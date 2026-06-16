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

## 实践复盘

本阶段完成了 `learning/LC_08_middleware/middleware_skeleton.py` 的手写实践：

- 补全了 `search_study_notes(...)`，用于根据阶段编号或笔记正文搜索本地学习笔记，并对空 query 做了简单保护。
- 补全了 `publish_study_summary(...)`，把“发布学习总结”模拟为一个有副作用的高影响工具，便于后续用 HITL 拦截。
- 继承 `AgentMiddleware` 实现了 `StudyLoggingMiddleware`，在 `before_agent`、`before_model`、`after_model`、`after_agent` 中打印 state、runtime、messages、最终消息和 tool calls 等观察信息。
- 在 `build_logging_agent()` 中通过 `middleware=[StudyLoggingMiddleware()]` 接入自定义日志中间件。
- 在 `build_hitl_agent()` 中通过 `HumanInTheLoopMiddleware(interrupt_on={"publish_study_summary": True})` 给 `publish_study_summary` 增加人工确认，并传入 `InMemorySaver()` 作为 checkpointer。
- 在 `invoke_hitl_until_interrupt(...)` 中使用固定 `thread_id` 和 `version="v2"` 发起 HITL 调用，观察中断结果。
- 补全了 `build_summarization_agent()` 的构造方式，明确 `SummarizationMiddleware` 需要传入 `model=model`、`trigger=...` 和 `keep=...`。当前 `main()` 中 summarization 仍作为后续可手动观察项保留。

### Logging middleware 观察结论

自定义 middleware 的类方法名是固定 hook 名称，本质上是重写 `AgentMiddleware` 父类方法（类似 Java 里继承父类后重写方法）。如果方法名写错，例如写成 `before_llm`，LangChain 不会把它当作 hook 调用。

实践中能观察到：

- `before_agent` 在一次 `agent.invoke(...)` 开始时执行，适合看入口 state 和 runtime。
- `before_model` 在每次模型调用前执行；如果 agent 先让模型决定工具调用、执行工具后再让模型生成最终回答，它可能执行多次。
- `after_model` 在模型返回后执行，很适合观察 `AIMessage` 以及其中的 `tool_calls`。
- `after_agent` 在 agent 完成后执行，适合观察最终消息。

`state` 在 middleware 中可以先按 dict-like 对象理解，常用：

```python
messages = state.get("messages", [])
```

`messages` 里的元素通常是 LangChain message 对象，例如 `HumanMessage`、`AIMessage`、`ToolMessage`，所以可以用：

```python
message.content
message.pretty_print()
getattr(message, "tool_calls", None)
```

这里也顺手复习了对象和字典的取值方式：

```text
对象：message.content 或 getattr(message, "content", "")
字典：state["messages"] 或 state.get("messages", [])
```

hook 返回值也很重要：

- 返回 `None`：只观察，不修改 agent state。
- 返回 `dict`：表示要更新 agent state。

学习过程中曾用实验性返回值观察行为，阶段收尾时已改回 `return None`。除非明确知道要更新哪些 state 字段，否则观察型 middleware 不建议返回任意 dict。

### HITL 观察结论

HITL 的关键结构是：

```python
HumanInTheLoopMiddleware(
    interrupt_on={"publish_study_summary": True}
)
```

这表示当 agent 准备执行 `publish_study_summary` 工具时，先暂停并要求人工确认。它拦截的是工具执行，不是用户输入本身。

实践中有三个配套点：

```python
checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "lc-08-hitl-demo"}}
version = "v2"
```

- `checkpointer` 保存暂停状态。
- `thread_id` 标识当前可恢复的对话线程。
- 中断和恢复必须使用同一个 `thread_id`。
- `version="v2"` 会让 `invoke(...)` 返回新版结果结构，便于读取 interrupt 信息。

一个重要观察是：普通 `agent.invoke(...)` 通常返回 dict；但带 `version="v2"` 的 HITL 调用会返回 `GraphOutput` 对象。它不是 dict，所以不能直接：

```python
result.keys()
```

应该通过：

```python
result.value
result.interrupts
```

来读取真正输出和中断信息。也就是说：

```text
普通 invoke：result 通常是 dict
HITL + version="v2"：result 是 GraphOutput，对象里包着 value 和 interrupts
```

因此 `inspect_result(...)` 最终被整理成同时兼容 dict 和 `GraphOutput` 的版本：先判断有没有 `value`、`interrupts` 属性，再决定从哪里取 messages 和 interrupts。

### Summarization 观察结论

`SummarizationMiddleware` 的核心目标不是“记忆”，而是“压缩当前上下文”。它适合在消息数量或 token 数变多时，把较早历史总结成短摘要，并保留最近若干条消息。

本阶段代码中使用的构造方式是：

```python
SummarizationMiddleware(
    model=model,
    trigger=("messages", 8),
    keep=("messages", 4),
)
```

其中：

- `model=model`：指定用于生成摘要的模型。
- `trigger=("messages", 8)`：消息数达到阈值时触发摘要。
- `keep=("messages", 4)`：摘要后保留最近 4 条消息。

这个 middleware 只解决上下文长度问题，不等于长期记忆。它可能丢失细节，所以用户偏好、关键事实、长期资料等内容后续仍要交给 LC-10 / LC-11 的 memory、checkpointer、store 来处理。

### 排错记录

#### `GraphOutput` 没有 `keys()`

HITL 实践中遇到过：

```text
AttributeError: 'GraphOutput' object has no attribute 'keys'
```

原因是调用时传了：

```python
version="v2"
```

返回值变成 `GraphOutput` 对象，而不是普通 dict。修正思路是：

```python
if hasattr(result, "value") and hasattr(result, "interrupts"):
    output = result.value
    interrupts = result.interrupts
else:
    output = result
    interrupts = ()
```

然后再从 `output` 中读取 `messages`。

#### PyCharm 黄色类型提示

实践中也遇到过 PyCharm 对 `agent.invoke(...)` 和 `create_agent(...)` 的黄色提示。主要原因是 LangChain 使用了装饰器、泛型、运行时注入和动态返回结构，IDE 的静态类型推断不一定能完全理解。

典型例子：

- `@tool` 包装后的函数，在运行时可以作为工具传给 `create_agent(...)`，但 IDE 有时推断不准确。
- `ToolRuntime[UserContext]` 这类注入参数对运行时没问题，但静态检查器不一定知道它由框架注入。
- `version="v2"` 返回 `GraphOutput`，不能当普通 dict 用。

这类问题的判断原则是：如果官方 API 用法正确、本地运行通过、ruff/语法检查通过，而黄色提示来自动态框架类型推断，就优先按运行时和官方文档理解。

### 代码检查

阶段收尾时执行了：

```powershell
.venv\Scripts\ruff.exe check learning\LC_08_middleware\middleware_skeleton.py
.venv\Scripts\python.exe -m py_compile learning\LC_08_middleware\middleware_skeleton.py
```

检查通过。收尾时做了几个小整理：

- `before_model(...)` 从实验性返回值改回 `return None`，避免观察型 middleware 意外修改 state。
- `search_study_notes(...)` 增加空 query 保护，避免空字符串误命中第一条笔记。
- 拆分过长打印语句，保持 ruff 检查通过。

### 练习点覆盖检查

对照本阶段实践任务：

| 练习点 | 状态 | 说明 |
| --- | --- | --- |
| 本地学习笔记搜索工具 | 已覆盖 | `search_study_notes(...)` 已支持阶段编号和正文关键词命中 |
| 高影响发布工具 | 已覆盖 | `publish_study_summary(...)` 已模拟发布动作 |
| 自定义 logging middleware | 已覆盖 | 已实现 `before_agent` / `before_model` / `after_model` / `after_agent` |
| 创建 logging agent | 已覆盖 | 已通过 `middleware=[StudyLoggingMiddleware()]` 接入 |
| HITL middleware | 已覆盖 | 已通过 `HumanInTheLoopMiddleware(interrupt_on=...)` 拦截发布工具 |
| checkpointer + thread_id | 已覆盖 | 已使用 `InMemorySaver()` 和固定 `thread_id` |
| HITL 中断结构观察 | 已覆盖 | 已观察并处理 `GraphOutput.value` / `GraphOutput.interrupts` |
| summarization 构造方式 | 已覆盖基础 | 已完成 `build_summarization_agent()`；更系统的上下文压缩观察留到 LC-09 / LC-10 前后继续加深 |

## 阶段总结

LC-08 的关键不是“再加一个工具”，而是理解 agent 运行过程中有哪些固定控制点。middleware 让日志、人工确认、摘要、动态 prompt、工具过滤等横切逻辑可以集中挂到 agent loop 上，而不是散落在每个工具或每次调用周围。

最重要的三个结论：

1. 自定义 middleware 通过固定 hook 方法接入 agent loop；方法名和返回值结构都要按接口约定来。
2. HITL 适合保护有副作用的工具；它依赖 checkpointer 保存暂停状态，并通过 `thread_id` 找回同一条可恢复执行。
3. summarization 是上下文压缩，不是长期记忆；它解决“对话越来越长”的成本问题，但不能替代后续 memory/store。

这一阶段也补上了 Python 装饰器和方法重写的直觉：`@tool`、middleware 装饰器和 `AgentMiddleware` 子类，本质上都是让普通 Python 函数或类方法进入框架约定的执行位置。可以把装饰器粗略理解成显式包装或注册函数；在横切逻辑场景下，它和 Java AOP 有相似味道，但 Python 装饰器更显式、更轻量。

## 和后续阶段的关系

- LC-09 上下文工程：会继续研究如何用 middleware 动态控制 prompt、工具选择和上下文成本。
- LC-10 Short-term Memory：会系统学习 `thread_id`、checkpointer 和线程内消息历史。
- LC-11 Long-term Memory：会区分摘要、短期记忆和跨会话长期记忆。
- LC-16 LangSmith Tracing：会把手写 `print` 日志升级为可视化 trace 和运行观测。
