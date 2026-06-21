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

- client 启动本地 server 子进程；不需要端口或 HTTP 服务
- 双方通过标准输入（std in）和标准输出（std out）传输 MCP 消息；
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

### 5.1 构造 `MultiServerMCPClient`

`build_mcp_client()` 是本仓库为了拆分职责而定义的普通封装函数，不是 LangChain 官方 API；它内部使用的 `MultiServerMCPClient(...)` 才是本阶段关键 API。

本地 `stdio` server 的完整客户端配置如下：

```python
import sys
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient


SERVER_PATH = Path(__file__).with_name("study_mcp_server_skeleton.py").resolve()


def build_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "study": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(SERVER_PATH)],
            }
        }
    )
```

配置字段含义：

| 字段 | 含义 |
| --- | --- |
| `"study"` | 当前 MCP server 在 client 配置中的名称，后续可用于选择 session 或区分多个 server |
| `"transport": "stdio"` | 使用子进程的标准输入和标准输出传输 MCP 消息 |
| `"command": sys.executable` | 使用运行当前 client 的同一个 Python 解释器，避免 server 脱离当前虚拟环境 |
| `"args": [str(SERVER_PATH)]` | 传给 Python 解释器的命令行参数，即需要启动的 MCP server 文件 |

client 创建 server 子进程的效果近似于：

```powershell
当前虚拟环境的Python.exe study_mcp_server_skeleton.py
```

完整调用关系是：

```text
build_mcp_client()
  -> MultiServerMCPClient(connection_config)
  -> await client.get_tools()
  -> client 启动 server 子进程
  -> 建立并初始化 MCP session
  -> 读取 MCP tool definitions
  -> 转换为 LangChain tools
```

这里使用 `sys.executable`，而不直接写 `"python"`，是为了确保 client 与 server 使用同一个虚拟环境及其中安装的依赖。

### 5.2 加载 MCP tools

构造 client 本身不会立即得到工具；需要在异步函数中调用：

```python
client = build_mcp_client()
tools = await client.get_tools()
```

`get_tools()` 会连接配置中的 MCP server、读取其工具定义，并返回可直接交给 agent 的 LangChain tools：

```python
agent = create_agent(model=model, tools=tools)
```

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

### 12.1 本地 MCP server

学习者完成了两个 MCP tools：

- `search_study_notes(query)`：对 query 做标准化后执行不区分大小写的完整子字符串匹配；空查询直接返回空列表，避免空字符串命中全部资料。
- `get_stage_summary(stage_id)`：统一去除首尾空格并转为大写，按阶段 ID 精确查询；未找到时返回标准化 ID。

server 使用：

```python
mcp.run(transport="stdio")
```

运行时由 client 启动为独立子进程，通过 stdin/stdout 传输 MCP 协议消息。server 没有向 stdout 写入普通调试输出。

### 12.2 MCP client 与异步调用

学习者使用 `MultiServerMCPClient` 配置本地 server：

```python
{
    "study": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(SERVER_PATH)],
    }
}
```

其中 `sys.executable` 确保 server 使用当前虚拟环境的 Python。随后完成：

```python
tools = await client.get_tools()
agent = create_agent(model, tools, system_prompt=...)
result = await agent.ainvoke({"messages": [...]})
```

同步入口通过 `asyncio.run(run_demo())` 启动事件循环。

### 12.3 工具发现与 agent 调用

`client.get_tools()` 成功发现并转换：

- `search_study_notes`
- `get_stage_summary`

agent 首先调用 `search_study_notes`，query 为 `LC-14 RAG 路径`。由于当前实现采用完整子字符串匹配，而资料中没有连续出现这段完整文本，因此工具正常执行但返回：

```python
{"query": "LC-14 RAG 路径", "matches": []}
```

此时 `ToolMessage.status == "success"`，说明工具执行成功；`matches=[]` 只是业务上的未命中。随后 agent 改用 `get_stage_summary(stage_id="LC-14")` 并成功获得资料，体现了首次检索未命中后更换工具的 agent 行为。

### 12.4 content、artifact 与 structured content

工具返回的 Python dict 经各层转换：

```text
Python dict
-> MCP CallToolResult.structuredContent
-> adapter artifact["structured_content"]
-> ToolMessage.artifact
```

实际观察到：

```python
{
    "structured_content": {
        "found": True,
        "note": {
            "stage_id": "LC-14",
            "topic": "Agentic / Hybrid RAG",
            "summary": "...",
        },
    }
}
```

其中：

- `structuredContent` 是 MCP `CallToolResult` 的协议字段；
- `structured_content` 是 `langchain-mcp-adapters` 的 `MCPToolArtifact` 包装键；
- `found`、`note` 等内层字段来自 MCP tool 自身的返回值。

最终回答的核心区别来自命中的工具摘要；模型还对适用场景做了合理扩写。本阶段目标是验证 MCP 工具链路和消息转换，并不要求像 grounded RAG 一样严格限制回答只能逐字来自工具资料。

## 13. 排错记录

### 13.1 agent 输入不能直接传字符串

错误写法：

```python
await agent.ainvoke("问题")
```

`create_agent(...)` 返回的是 graph，需要传入包含 `messages` 的状态字典：

```python
await agent.ainvoke(
    {
        "messages": [
            {"role": "user", "content": "问题"},
        ]
    }
)
```

否则可能出现 `InvalidUpdateError: Expected dict`。

### 13.2 完整子字符串匹配导致组合 query 未命中

`search_study_notes` 判断整个标准化 query 是否连续存在于资料文本中：

```python
normalized_query in " ".join(note.values()).lower()
```

因此资料分别含有 `LC-14`、`RAG` 和相关描述，并不代表组合 query `LC-14 RAG 路径` 能命中。这是当前教学搜索算法的预期限制，不是 MCP 调用失败。

### 13.3 transport/session 错误与业务结果不同

临时写错 server 路径时，Python 子进程无法启动目标文件，stdio 连接随子进程退出而关闭。错误发生在 `await client.get_tools()` 的连接或 session 初始化阶段：

- client 直接抛出异常；
- agent 尚未完成工具加载；
- 不会产生 `ToolMessage`。

这与正常返回 `matches=[]` 不同，后者仍是 `ToolMessage(status="success")`。

### 13.4 MCP tool 主动失败

让 MCP tool 主动抛出异常后，FastMCP 将其表示为 `CallToolResult(isError=True)`；当前 `langchain-mcp-adapters==0.3.0` 默认把该执行错误交回 agent：

```text
ToolMessage.status == "error"
```

agent 可以读取错误后继续回答或自我修正。transport/session 错误不属于该范围，仍会直接抛出。

## 14. 阶段总结

本阶段完成了本地 MCP 最小闭环：

```text
FastMCP server
-> stdio transport
-> MultiServerMCPClient
-> LangChain tools
-> create_agent
-> AIMessage / ToolMessage
```

核心结论：

1. MCP server 是独立进程，client 与 server 不共享 Python 内存，只通过协议交换可序列化数据。
2. `stdio` 由 client 启动 server 子进程，并使用 server 的 stdin/stdout 通信；stdout 不应混入普通打印。
3. `MultiServerMCPClient` 负责连接 server、发现 MCP tools 并转换为 LangChain tools。
4. MCP I/O 使用异步 API，核心入口是 `await client.get_tools()`、`await agent.ainvoke(...)` 和 `asyncio.run(...)`。
5. 默认 client 调用采用无状态 session；显式持久 session 与 LangGraph `thread_id` 是不同层次的生命周期概念。
6. `ToolMessage.content` 面向消息流和模型，`artifact["structured_content"]` 保留 MCP structured content。
7. 未命中是成功的业务结果，tool 执行异常可变为 `status="error"`，transport/session 失败则直接抛出异常。

后续 LC-16 LangSmith Tracing 将观察一次 agent 运行中的模型调用、MCP tool call 和消息链路。

