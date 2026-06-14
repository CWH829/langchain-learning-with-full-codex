# LC-04：Messages

## 本阶段目标

这一阶段先把“模型看到的上下文”拆开看清楚。学完后，你应该能回答三个问题：

1. LangChain v1 里的 message 是什么？
2. `SystemMessage`、`HumanMessage`、`AIMessage`、`ToolMessage` 分别表达什么角色？
3. `content`、`text`、`content_blocks`、`tool_calls`、`usage_metadata` 这些字段应该怎么看？

## 官方资料核对

已核对 LangChain 官方文档：

- Messages：<https://docs.langchain.com/oss/python/langchain/messages>

关键结论：

- Messages 是 LangChain 中模型上下文的基本单位，承载 role、content 和 metadata。
- chat model 可以接收普通字符串，也可以接收 message 列表；有系统指令、多轮上下文、多模态内容时，应优先理解 message 列表。
- 官方当前导入路径是 `from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage`。
- 如果需要给函数参数或列表做通用类型标注，`BaseMessage` 应从 `langchain_core.messages` 导入。
- `model.invoke(...)` 返回的是 `AIMessage`，不是普通字符串。
- `AIMessage` 里除了文本，还可能包含 `tool_calls`、`usage_metadata`、`response_metadata` 等结构化信息。
- `content` 是原始内容载荷；`content_blocks` 是 LangChain 尝试标准化后的内容块表示。

## 核心概念

### message 是模型上下文里的“一条记录”

在 LC-03 里，我们把 model 当作一个可替换的远程服务客户端。到了 LC-04，可以把传给模型的输入理解成一组消息记录：

```text
[
  系统规则,
  用户问题,
  助手历史回答,
  用户追问,
]
```

模型不是只看“最后一句话”，而是看你传给它的上下文列表。列表越长，模型拿到的上下文越多，成本也可能越高。

从 LangChain 本身看，可以先把 message 拆成几层：

| 层次 | 说明 |
| --- | --- |
| message class | 消息类型，例如 `SystemMessage`、`HumanMessage`、`AIMessage` |
| role / type | 消息在对话里的角色，用来区分系统规则、用户输入、模型输出或工具结果 |
| content | 消息主体内容，可能是字符串，也可能是内容块列表 |
| metadata | 调用返回的附加信息，例如 token 用量、模型名、finish reason |
| message list | 按顺序排列的上下文，模型会基于这组上下文生成下一条 `AIMessage` |

### 四种常见消息

| 类型 | 角色 | 典型用途 |
| --- | --- | --- |
| `SystemMessage` | 系统/开发者规则 | 定义助手行为、边界、风格 |
| `HumanMessage` | 用户输入 | 用户问题、指令、补充信息 |
| `AIMessage` | 模型输出 | 模型生成的回答，或模型提出的工具调用 |
| `ToolMessage` | 工具结果 | 把某次工具调用的执行结果交回模型 |

这一节先重点掌握前三个。`ToolMessage` 会在 LC-05 Tools 里更自然地接上，因为它必须和 `AIMessage.tool_calls` 里的 `id` 对齐。

## 字符串输入和 messages 输入

最简单调用可以直接传字符串：

```python
response = model.invoke("用一句话解释 LangChain message。")
```

这适合一次性问题。缺点是系统规则和历史上下文不够清晰。

更推荐本阶段手写的是 message 列表：

```python
from langchain.messages import HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage

messages: list[BaseMessage] = [
    SystemMessage("你是一个简洁的中文学习助手。"),
    HumanMessage("用一句话解释 LangChain message。"),
]

response = model.invoke(messages)
```

这里 `response` 是 `AIMessage`。打印文本时优先看：

```python
print(response.text)
```

如果你想分析结构，再看：

```python
print(response.content)
print(response.content_blocks)
print(response.usage_metadata)
print(response.response_metadata)
```

## content 与 content_blocks

可以先用一句话区分：

- `content`：消息原始内容，可能是字符串，也可能是 provider 原生格式的列表。
- `content_blocks`：LangChain 尝试整理出的标准内容块列表，便于跨 provider 分析。

普通文本模型调用里，`content` 往往就是字符串。到多模态、reasoning、tool calling 或引用信息时，`content_blocks` 的价值会更明显。

本阶段不需要急着写图片、音频或文件输入；先会看纯文本消息结构就够了。

## 关键字段细节

### `content`

`content` 是 message 的原始内容。最常见情况是字符串：

```python
HumanMessage(content="message 和普通字符串 prompt 有什么区别？")
```

在更复杂的场景里，`content` 也可能是列表，列表中包含文本块、图片块、工具调用块或 provider 自己的扩展结构。LC-04 先掌握字符串内容即可；后续多模态、工具调用和 reasoning 输出再继续展开。

### `text`

`text` 是从 message 里提取出的纯文本视图。当前 `langchain-core` 中推荐使用属性访问：

```python
print(message.text)
```

旧代码里可能会看到：

```python
print(message.text())
```

当前版本为了兼容旧写法仍支持 `text()`，但新代码优先写 `message.text`。如果 `content` 是列表，`text` 会尽量抽取其中的文本块；非文本块会被忽略。

### `content_blocks`

`content_blocks` 是 LangChain 对消息内容做出的标准化内容块视图。普通文本通常会变成类似：

```python
[{"type": "text", "text": "..."}]
```

它的价值在于：当 provider 返回的不只是纯文本时，`content_blocks` 更适合做结构化观察。例如后续可能看到 `tool_call`、reasoning、server tool、image、file 等内容块。不同 provider 的原始格式可能不同，LangChain 会尽量把它们整理成更统一的结构。

### `usage_metadata`

`usage_metadata` 通常出现在模型返回的 `AIMessage` 上，用于记录 token 用量，例如输入 token、输出 token、总 token 等。这个字段很适合用来观察一次调用的成本。

输入侧的 `SystemMessage`、`HumanMessage` 通常没有这个字段，或者值为 `None`。这是合理的：它们只是你构造出来的上下文记录，并不是 provider 返回的调用结果。

### `response_metadata`

`response_metadata` 也是模型返回消息上的常见字段，通常包含 provider 返回的附加信息，例如模型名、结束原因、请求 id、底层响应信息等。它不一定跨 provider 完全一致，所以排错时有价值，业务逻辑里不要过早依赖它的具体结构。

### `tool_calls`

`tool_calls` 主要出现在 `AIMessage` 上，表示模型希望调用哪些工具。LC-04 只需要知道它存在；LC-05 Tools 会重点学习它如何和工具函数、`ToolMessage` 连接起来。

## 消息顺序

message 列表是有顺序的。一般按对话发生顺序排列：

```python
messages = [
    SystemMessage(content="请用简洁中文回答问题。"),
    HumanMessage(content="第一个问题"),
    AIMessage(content="第一次回答"),
    HumanMessage(content="追问"),
]
```

模型会基于这组上下文生成下一条 `AIMessage`。如果顺序错了，模型看到的上下文逻辑就会错。系统消息通常放在最前面，用来设定整体行为；用户消息表示当前问题；历史 AI 消息表示模型之前说过什么。

## 手写实践任务

请你亲手完成 `learning/LC_04_messages/message_flow_skeleton.py`：

1. 复用 LC-03 的 `build_chat_model()` 创建模型。
2. 用 `SystemMessage` 和 `HumanMessage` 构造一个最小 message 列表。
3. 调用 `model.invoke(messages)`。
4. 写一个 `print_message(message)` 辅助函数，打印：
   - message 的 Python 类型名
   - `content`
   - `text`
   - `content_blocks`
   - `usage_metadata`
5. 观察 `SystemMessage`、`HumanMessage` 和模型返回的 `AIMessage` 在字段上的差异。

建议问题：

```text
请用两句话解释 LangChain 的 message，并说明它和普通字符串 prompt 的区别。
```

## Python 要点：list / dict / 对象属性访问

这一节会同时看到三种数据访问方式：

```python
messages[0]
```

```python
tool_call["name"]
```

```python
response.content
```

简单区分：

| 写法 | 对象类型倾向 | 关注点 |
| --- | --- | --- |
| `messages[0]` | list | 按位置取第几条消息 |
| `tool_call["name"]` | dict | 按 key 取结构化字段 |
| `response.content` | Python 对象属性 | 读取 message 对象上的属性 |

以后读 LangChain 示例时，经常会混用这三种写法。先看清“当前变量到底是什么类型”，比硬背 API 更重要。

## 常见坑

- 把 `AIMessage` 当成普通字符串遍历。它是对象，打印文本优先用 `response.text`。
- 以为 system prompt 每次都会自动存在。只有你传入 `SystemMessage` 或 agent 配置里有 system prompt，模型才会看到这类规则。
- 忽略 message 顺序。多轮上下文通常按时间顺序排列，顺序会影响模型理解。
- 过早研究所有 content block 类型。先掌握文本、metadata、tool_calls，再进入多模态和工具调用会更稳。
- 混淆 `langchain.messages` 和 `langchain_core.messages` 的导入边界。具体消息类从 `langchain.messages` 导入即可；通用基类 `BaseMessage` 应从 `langchain_core.messages` 导入。
- 给列表只标 `list`，会丢失元素类型信息。更清晰的写法是 `messages: list[BaseMessage] = [...]`。
- 以为 `usage_metadata` 每条 message 都有值。通常只有模型返回的 `AIMessage` 才更可能带 token 用量。

## 本阶段完成标准

- 能解释 message 是模型上下文里的基本单位。
- 能说清 `SystemMessage`、`HumanMessage`、`AIMessage`、`ToolMessage` 的职责。
- 能用 message 列表调用模型，而不是只传字符串。
- 能打印并观察 `AIMessage` 的 `content`、`text`、`content_blocks` 和 metadata。
- 能区分 list 下标、dict key、对象属性这三种访问方式。

## 实践复盘

2026-06-14：

本阶段你已经补全 `learning/LC_04_messages/message_flow_skeleton.py`，完成了 LC-04 的最小实践链路：

1. 复用 LC-03 的 `build_chat_model()` 创建模型，没有在 LC-04 里重复模型配置逻辑。
2. 用 `SystemMessage` 设置回答风格：`请用简洁中文回答问题。`
3. 用 `HumanMessage` 表达用户问题：`message 和普通字符串 prompt 有什么区别？`
4. 用 `list[BaseMessage]` 作为函数返回类型，表达“这是多种 message 的统一列表”。
5. 用 `model.invoke(messages)` 把 message 列表传给模型，观察返回的 `AIMessage`。
6. 用 `print_message(message)` 打印类型名、`content`、`text`、`content_blocks`、`usage_metadata`，开始从“只看文本”转向“观察消息对象结构”。

你这次代码里的核心理解是对的：输入消息和输出消息虽然都叫 message，但字段价值不同。

- `SystemMessage` / `HumanMessage`：主要承载你提供给模型的上下文，重点看 `content`、`text`、`content_blocks`。
- `AIMessage`：模型返回结果，除了文本内容，还可能带 `usage_metadata`、`response_metadata`、`tool_calls` 等运行时信息。

有一个可选打磨点：当前代码里写的是 `msgs : list = [...]`。能运行，但类型信息不够精确。后续可以改成：

```python
msgs: list[BaseMessage] = [
    SystemMessage(content="请用简洁中文回答问题。"),
    HumanMessage(content="message 和普通字符串 prompt 有什么区别？"),
]
```

这不是必须修复的错误，只是更利于 IDE 和自己阅读。冒号前也不需要空格，Python 常见风格是 `msgs: list[BaseMessage]`。

## 阶段总结

LC-04 的重点不是“怎么让模型回答”，而是“模型到底看到了什么结构”。从这一节开始，prompt 不再只是一个字符串，而是一组有角色、有顺序、有元数据的消息对象。

本阶段最重要的结论：

1. `message` 是 LangChain 模型上下文的基本单位。
2. `SystemMessage` 用来放系统规则，`HumanMessage` 用来放用户输入，`AIMessage` 用来表示模型输出，`ToolMessage` 用来承载工具结果。
3. `model.invoke(...)` 可以接收字符串，也可以接收 message 列表；需要系统规则、多轮上下文或结构化观察时，优先理解 message 列表。
4. `model.invoke(messages)` 返回的是 `AIMessage` 对象，不是普通字符串。
5. 看最终文本时用 `message.text`；看原始载荷时用 `message.content`；看标准化结构时用 `message.content_blocks`。
6. `usage_metadata` 和 `response_metadata` 是观察成本、排错和理解 provider 返回的重要入口。
7. `ToolMessage` 和 `AIMessage.tool_calls` 的关系先留到 LC-05 Tools 继续展开。

下一阶段 LC-05 会在 messages 的基础上进入 tools：模型不只返回文本，还可能在 `AIMessage` 里提出工具调用请求，然后程序执行工具，再把工具结果作为 `ToolMessage` 放回上下文。

## 建议 Git commit message

```text
LC-04：完成 Messages 阶段学习
```
