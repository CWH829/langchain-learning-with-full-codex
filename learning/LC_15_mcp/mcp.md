# LC-15：MCP

## 1. 本阶段目标

完成本阶段后，应能：

1. 解释 MCP client、MCP server、transport 与 LangChain agent 的职责边界。
2. 用 Python 启动一个本地 `stdio` MCP server，并暴露学习资料查询工具。
3. 用 `MultiServerMCPClient` 加载 MCP tools，再交给 `create_agent(...)`。
4. 使用 `async def`、`await`、`asyncio.run(...)` 完成异步调用。
5. 从 agent 返回的 messages 中观察 `AIMessage.tool_calls`、`ToolMessage` 和最终回答。
6. 理解默认无状态 MCP session 与显式持久 session 的区别。

本阶段先完成最小工具链路：

```text
用户问题
  -> LangChain agent
  -> MCP adapter 转换后的 LangChain tool
  -> stdio transport
  -> 本地 MCP server
  -> 查询学习资料
  -> ToolMessage
  -> agent 最终回答
```

## 2. 官方文档核对

本阶段以以下官方资料为准：

- [LangChain MCP 文档](https://docs.langchain.com/oss/python/langchain/mcp)
- [langchain-mcp-adapters GitHub](https://github.com/langchain-ai/langchain-mcp-adapters)
- [MCP 官方文档](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

当前项目锁定：

- `langchain==1.3.9`
- `langchain-mcp-adapters==0.3.0`
- 间接依赖 `mcp==1.27.2`

当前环境可使用：

```python
from mcp.server.fastmcp import FastMCP
```

LangChain 最新文档中的部分示例改用独立的 `fastmcp` 包。本阶段不为追随示例额外增加依赖，而是使用项目已经锁定的 MCP Python SDK。

`langchain-mcp-adapters==0.3.0` 的几个关键行为：

- `MultiServerMCPClient.get_tools()` 会把 MCP tools 转成 LangChain tools。
- client 默认按**无状态**方式工作，每次工具调用创建并清理 MCP session。
- MCP tool 返回错误时，默认可转换为 `ToolMessage(status="error")` 交给模型处理。
- transport、session 或内容转换错误仍会直接抛出异常。
- MCP structured content 可通过 `ToolMessage.artifact` 观察。

## 3. MCP 解决什么问题

普通 LangChain tool 通常直接存在于 agent **应用**进程中：

```text
agent 进程
├── model
├── agent loop
└── Python tool function
```

MCP 把“能力提供方”和“能力使用方”拆开：

```text
Host / LangChain 应用
├── agent
└── MCP client
      |
      | transport
      v
MCP server
├── tools
├── resources
└── prompts
```

因此 MCP 的核心价值不是让工具函数更短，而是形成统一的外部能力协议：

- server 可以独立开发和运行；
- client 不必理解工具内部实现；
- 不同 AI 应用可以复用同一个 server；
- 工具、资源和 prompts 可以通过统一协议发现与调用。

## 4. 四个核心角色

### 4.1 Host

Host 是承载用户体验和 agent 的**应用**。本阶段中，运行 LangChain agent 的 Python 脚本就是 host。

### 4.2 MCP client

client 负责连接 MCP server、发现能力并发起调用。

```python
client = MultiServerMCPClient({...})
tools = await client.get_tools()
```

`tools` 对 agent 来说仍然是熟悉的 LangChain tools。协议转换由 adapter 完成。

### 4.3 MCP server

server 独立**暴露 tools**、resources 或 prompts。本阶段只实践 tools：

```python
mcp = FastMCP("langchain-study")

@mcp.tool()
def search_study_notes(query: str) -> dict[str, object]:
    ...
```

### 4.4 Transport

transport 决定 client 与 server 如何**通信**。

本阶段使用 `stdio`：

- client 启动本地 server 子进程；
- 双方通过标准输入和标准输出传输 MCP 消息；
- 适合本地工具和最小学习示例；
- server 不应随意向 stdout 打印调试文本，以免污染协议消息。

HTTP transport 更适合独立部署、远程访问和认证，但不作为本阶段手写重点。

## 5. MCP tools 与 LangChain tools

MCP server 描述工具的名称、说明和输入 schema。adapter 读取这些定义后，将其**转换为 LangChain tool**：

```text
@mcp.tool()
    -> MCP tool schema
    -> client.get_tools()
    -> LangChain BaseTool
    -> create_agent(model, tools)
```

模型并不知道工具最初是普通 `@tool`，还是来自 MCP server。对模型而言，关键仍是：

- 工具名是否清楚；
- docstring 是否能说明何时调用；
- 参数名与类型是否明确；
- 返回结果是否足够可靠。

## 6. 为什么本阶段使用 async/await

MCP client 涉及进程、网络或 session I/O，因此核心 API 是异步的：

```python
async def main() -> None:
    tools = await client.get_tools()
    result = await agent.ainvoke(...)


if __name__ == "__main__":
    asyncio.run(main())
```

可以先这样理解：

- `async def`：声明一个**异步函数**，调用后不会直接得到最终结果。
- `await`：等待异步操作完成，同时允许事件循环处理其他任务。
- `asyncio.run(...)`：从普通同步入口启动事件循环。
- `ainvoke(...)`：`invoke(...)` 的异步版本。

`await` 只能直接出现在 `async def` 内部。

## 7. 客户端与 session 生命周期

### 7.1 默认无状态调用

```python
client = MultiServerMCPClient({...})
tools = await client.get_tools()
```

默认情况下，每次 tool invocation 会创建新 session，调用后清理。这个模式适合：

- 工具调用彼此独立；
- server 不依赖前一次调用留下的临时状态；
- 希望减少手动生命周期管理。

### 7.2 显式持久 session

需要让**多次调用共享**同一个 session 时，可以显式管理：

```python
async with client.session("study") as session:
    tools = await load_mcp_tools(session)
    ...
```

本阶段先理解该边界，不要求实现 stateful server。不要把 MCP session 与 LangGraph 的 `thread_id` 混为一谈：

- MCP session 管理 client 与 server 的协议连接状态；
- `thread_id` 管理 LangGraph checkpointer 中的对话状态。

## 8. Structured content 与 ToolMessage

MCP tool 可以返回**结构化数据**。adapter 会将其转换成 agent 可使用的工具结果；结构化部分可出现在 `ToolMessage.artifact` 中。

观察时应区分：

- `ToolMessage.content`：进入消息历史、给模型阅读的**内容**；
- `ToolMessage.artifact`：应用侧可读取的附加**结构化数据**；
- 最终 `AIMessage`：模型根据工具结果生成的自然语言回答。

这与 LC-14 的 `content_and_artifact` 思路相似，但这里的**原始结果**来自独立 MCP server。

## 9. 手写实践任务

### 任务 A：完成 MCP server

文件：`study_mcp_server_skeleton.py`

1. 阅读 `STUDY_NOTES` 的数据结构。
2. 补全 `search_study_notes(...)`，按 query 匹配学习资料。
3. 补全 `get_stage_summary(...)`，按阶段 ID 返回单条资料。
4. 保持 `mcp.run(transport="stdio")` 作为服务入口。
5. 不在 server 的 stdout 中添加普通 `print(...)`。

### 任务 B：加载 MCP tools

文件：`mcp_agent_skeleton.py`

1. 用当前 Python 解释器启动 server。
2. 构造 `MultiServerMCPClient`。
3. 使用 `await client.get_tools()` 加载工具。
4. 打印工具名称、说明和参数 schema。

### 任务 C：让 agent 调用 MCP tool

1. 将 MCP tools 传给 `create_agent(...)`。
2. 使用 `await agent.ainvoke(...)` 提问。
3. 准备至少一个需要查询资料的问题。
4. 遍历返回 messages，观察 tool call、tool result 和最终回答。

### 任务 D：观察失败边界

完成主链路后，可任选一个小实验：

- 请求不存在的阶段 ID，观察工具如何返回“未找到”；
- 临时写错 server 路径，观察 transport/session 错误；
- 让工具主动返回错误结果，观察 `ToolMessage.status`。

不要一次制造多个错误，否则不容易判断异常发生在哪一层。

## 10. 建议观察记录

实践时记录：

1. `client.get_tools()` 返回了哪些工具？
2. 每个工具的 `name`、`description`、`args_schema` 是什么？
3. agent 是否一次就选择了正确工具？
4. `AIMessage.tool_calls` 中有哪些参数？
5. `ToolMessage.content` 与 `artifact` 分别是什么？
6. 最终回答是否忠实于 MCP server 返回的资料？
7. server 路径错误与普通 tool 业务错误的表现有何不同？

## 11. 当前阶段边界

本阶段暂不展开：

- 远程 Streamable HTTP server 部署；
- OAuth、headers 与生产认证；
- MCP resources 和 prompts 的完整实践；
- tool interceptors；
- progress、logging、elicitation；
- 多 server 的复杂编排；
- stateful MCP server。

这些能力先知道存在即可。当前最重要的是跑通并解释：

```text
server 暴露工具
-> client 发现并转换工具
-> agent 选择工具
-> MCP 完成远程式调用
-> 结果回到消息流
```

## 12. 实践记录

待学习者完成代码后补充。

## 13. 排错记录

待实践后补充。

## 14. 阶段总结

待实践后补充。
