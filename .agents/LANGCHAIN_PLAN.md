# LangChain 系统学习计划

## 0. 文件用途

本文件是 Codex 项目中的长期学习路线图与状态文件，放在 `.agents/` 下作为 agent 优先读取的项目上下文。每次新会话开始时，Codex Agent 先读取本文件，再按当前进度推进学习，不需要重复解释背景。

## 1. 元信息

| 字段 | 值 |
| --- | --- |
| 计划版本 | v0.1 |
| LangChain 基线 | LangChain v1，当前锁定 `langchain==1.3.9` |
| 主学习语言 | Python |
| 学习者背景 | Java 开发者，Python 基础较薄弱 |
| 项目语境 | Codex project |
| 学习方式 | 问答讲解 + Python 代码实践 + Git 记录 |
| 学习时长 | 未指定 |
| 学习深度 | 先达到能独立完成 agent、RAG、MCP、trace/eval 小项目 |
| 更新时间 | 2026-06-13 |

## 2. Codex Agent 执行说明

1. 先读本文件，找到“知识点总表”中第一条 `未开始` 或 `进行中` 的任务。
2. 学习每个知识点前，优先检索官方文档，确认 API、包名、导入路径未过时。
3. 每个知识点按：`资料确认 -> 中文讲解 -> 代码实践 -> 练习 -> 总结 -> 更新进度 -> 建议 Git 提交` 推进。
4. 代码以 Python 为主；遇到 Python 语法、项目结构、依赖管理、异步、类型标注等内容时，面向 Java 开发者补充说明。
5. 每次完成任务后，更新本文件中的状态、开始时间、完成时间和备注。
6. 学习计划变化时，只修改必要内容，并在“变更记录”中追加摘要；该表只记录计划本身的变更，不记录项目代码、目录或提交历史的普通变更。同一阶段的多次计划调整可以合并成一条记录，并在单元格内用序号列出。
7. 为节省 token，不要一次性展开所有知识点；只展开当前任务需要的资料和代码。
8. 本项目中的代码注释、Git 提交信息等优先使用中文。

状态枚举：`未开始` / `进行中` / `已完成` / `跳过`

时间格式：`YYYY-MM-DD` 或 `YYYY-MM-DD HH:mm`

## 3. 环境与命令

```bash
# 接入 LangChain 官方文档 MCP
codex mcp add langchain-docs --url https://docs.langchain.com/mcp

# 初始化 Python 项目
uv init

# 基础依赖
uv add langchain==1.3.9 langgraph==1.2.5 langchain-mcp-adapters==0.3.0

# 开发依赖
uv add --dev pytest==9.0.3 ruff==0.15.17

# 同步依赖
uv sync
```

模型 provider、API key、额外集成包按实际学习任务再安装，不在初始计划中固定。

## 4. 建议项目结构

```text
.
├── LANGCHAIN_PLAN.md                 # 根目录入口说明
├── .agents/
│   └── LANGCHAIN_PLAN.md             # agent 优先读取的学习计划
├── README.md
├── pyproject.toml
├── src/
│   └── langchain_study/
├── examples/
│   ├── 01_hello_agent.py
│   ├── 02_tools_agent.py
│   ├── 03_structured_output.py
│   ├── 04_memory.py
│   ├── 05_rag.py
│   ├── 06_mcp.py
│   └── 07_langsmith_eval.py
├── notes/
│   ├── 01_version_boundary.md
│   ├── 02_core_components.md
│   ├── 03_tools.md
│   ├── 04_structured_output.md
│   ├── 05_memory.md
│   ├── 06_rag.md
│   ├── 07_mcp.md
│   ├── 08_langsmith.md
│   └── 09_langgraph.md
├── data/
└── tests/
```

## 5. 资料来源与优先级

| ID | 优先级 | 来源 | 用途 | 备注 |
| --- | --- | --- | --- | --- |
| R1 | P0 | LangChain Docs MCP | 让 Codex 查询最新官方文档 | 首选 |
| R2 | P0 | https://docs.langchain.com/use-these-docs | 官方机器可读文档入口 | 首选 |
| R3 | P0 | https://docs.langchain.com/oss/python/releases/langchain-v1 | 确认 v1 边界 | 必读 |
| R4 | P0 | https://docs.langchain.com/oss/python/langchain/overview | LangChain 主线 | 必读 |
| R5 | P0 | https://docs.langchain.com/oss/python/langchain/quickstart | 最小 agent 入门 | 必读 |
| R6 | P0 | LangChain agents / models / messages / tools / structured-output / memory / retrieval / MCP 官方页 | 主题学习 | 按需检索 |
| R7 | P0 | https://docs.langchain.com/langsmith/home | LangSmith tracing / observability | 工程化 |
| R8 | P0 | https://docs.langchain.com/langsmith/evaluation | LangSmith evaluation | 工程化 |
| R9 | P1 | https://docs.langchain.com/oss/python/langgraph/overview | LangGraph 进阶编排 | 后置 |
| R10 | P1 | https://docs.python.org/zh-cn/3/tutorial/index.html | Python 基础补课 | 按需 |
| R11 | P2 | RAG / ReAct / Toolformer / MCP spec | 理解模式来源 | 选读 |
| R12 | P3 | 中文社区资料 | 术语预览 | 需回到官方文档核对 |

## 6. 学习推进协议

每个知识点的单次学习输出尽量包含：

```text
1. 当前知识点目标
2. 官方资料确认
3. 核心概念讲解
4. Java 开发者视角类比
5. Python 代码实践
6. 练习题或小任务
7. 常见坑
8. 本次总结
9. 更新 LANGCHAIN_PLAN.md
10. 建议 Git commit message
```

建议 Git commit message 格式：

```text
study: complete <topic-id> <topic-name>
```

示例：

```text
study: complete LC-02 minimal create_agent
```

## 7. 知识点总表

| ID | 主题 | 知识点 | 最小目标 | 产出 | 代码实践 | Python 要点 | 状态 | 开始时间 | 完成时间 | 资源 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LC-00 | 项目初始化 | uv、项目结构、Git 规则 | 建好学习仓库 | 初始目录 + README | 初始化项目并首次提交 | venv/uv 与 Maven/Gradle 的区别 | 已完成 | 2026-06-13 | 2026-06-13 | R10 | 已创建 uv 兼容项目骨架；计划迁移到 `.agents/`；依赖改为 PyPI 最新精确版本。 |
| LC-01 | 版本边界 | LangChain v1、`create_agent`、`langchain-classic` | 识别新旧资料边界 | `notes/01_version_boundary.md` | 对比 v1 与旧教程导入路径 | 包名和导入路径优先查官方 | 未开始 |  |  | R3,R4 |  |
| LC-02 | 最小 agent | `create_agent`、model、tools | 跑通最小 agent | `examples/01_hello_agent.py` | 创建能回答问题并调用工具的 agent | 函数、模块、入口脚本 | 未开始 |  |  | R5 |  |
| LC-03 | Models | chat model、provider、参数 | 能替换模型 provider | `notes/02_core_components.md` | 封装可切换 model 配置 | 环境变量、配置读取 | 未开始 |  |  | R6 |  |
| LC-04 | Messages | system/user/assistant/tool messages、content blocks | 理解模型上下文结构 | message 示例笔记 | 打印并分析 messages 流 | list/dict、对象属性访问 | 未开始 |  |  | R6 |  |
| LC-05 | Tools | tool 定义、参数 schema、tool calling | 会写自定义工具 | `examples/02_tools_agent.py` | search + calculator 双工具 agent | docstring、type hints、异常处理 | 未开始 |  |  | R6 |  |
| LC-06 | Structured Output | `response_format`、Pydantic | 返回稳定结构 | `examples/03_structured_output.py` | 输出 `TaskPlan` / `StudySummary` | Pydantic 类似强类型 DTO | 未开始 |  |  | R6 |  |
| LC-07 | Runtime | runtime context、tool runtime | 理解运行期上下文 | runtime 示例 | 在工具中读取上下文 | 参数注入、可选参数 | 未开始 |  |  | R6 |  |
| LC-08 | Middleware | middleware、logging、HITL、summarization | 给 agent 加控制逻辑 | middleware 示例 | 加日志/摘要/人工确认 | 装饰器、函数式组合 | 未开始 |  |  | R6 |  |
| LC-09 | 上下文工程 | prompt、tool context、context lifecycle | 控制成本与行为 | 上下文策略文档 | 精简 system prompt + 按需加载资料 | 长文本拆分、上下文边界 | 未开始 |  |  | R6 |  |
| LC-10 | Short-term Memory | thread-scoped memory、checkpointer | 实现线程内记忆 | `examples/04_memory.py` | 多轮对话保留上下文 | `with`、资源管理 | 未开始 |  |  | R6 |  |
| LC-11 | Long-term Memory | store、跨会话记忆 | 区分短期/长期记忆 | memory 对比笔记 | 存取用户偏好示例 | 数据结构、序列化 | 未开始 |  |  | R6 |  |
| LC-12 | Retrieval 基础 | documents、splitters、embeddings、vector store | 能做语义检索 | retrieval demo | 文本切分 + 向量检索 | 文件读写、列表处理 | 未开始 |  |  | R6 |  |
| LC-13 | 2-step RAG | retrieve -> generate | 做最小知识问答 | `examples/05_rag.py` | 本地文本问答 | pipeline 思维 | 未开始 |  |  | R6,R11 |  |
| LC-14 | Agentic / Hybrid RAG | agentic retrieval、query rewrite、validation | 知道何时升级 RAG | RAG 对比笔记 | 给 agent 增加检索工具 | 控制流、结果校验 | 未开始 |  |  | R6,R11 |  |
| LC-15 | MCP | MCP、`langchain-mcp-adapters`、docs MCP | 接入外部工具/文档 | `examples/06_mcp.py` | 让 agent 调用 MCP server | async/await、客户端生命周期 | 未开始 |  |  | R1,R2,R6 |  |
| LC-16 | LangSmith Tracing | tracing、runs、observability | 能定位 agent 行为 | trace 截图/说明 | 记录一次完整 agent trace | 环境变量、SDK 配置 | 未开始 |  |  | R7 |  |
| LC-17 | LangSmith Evaluation | dataset、evaluator、experiment | 做最小离线评测 | `examples/07_langsmith_eval.py` | 对 RAG/agent 做 mini eval | 测试思维、函数返回结构 | 未开始 |  |  | R8 |  |
| LC-18 | LangGraph 入门 | graph、state、node、edge | 理解何时用 LangGraph | `notes/09_langgraph.md` | Router 或简单 workflow | TypedDict、状态传递 | 未开始 |  |  | R9 |  |
| LC-19 | Multi-agent | supervisor、handoff、subagent | 了解多 agent 设计边界 | multi-agent 笔记 | 可选 subagent demo | 上下文隔离 | 未开始 |  |  | R6,R9 | 可选 |
| LC-20 | 综合小项目 | agent + tools + RAG + MCP + tracing/eval | 完成可复盘项目 | mini project | 做一个个人知识库问答 agent | 项目组织、测试、提交 | 未开始 |  |  | R1-R9 |  |

## 8. Python 补充学习索引

| ID | 主题 | 触发场景 | 学习目标 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
| PY-01 | venv / uv | 初始化项目 | 理解 Python 依赖隔离 | 已完成 | uv 类比不放 README；后续学习时按需讲解。 |
| PY-02 | type hints | 写 tools / schema | 能读写常见类型标注 | 未开始 | Python 不像 Java 默认强制运行时类型 |
| PY-03 | Pydantic / dataclass | structured output | 会定义轻量数据模型 | 未开始 | 类似 DTO/POJO |
| PY-04 | decorators | tool / middleware | 理解装饰器包装函数 | 未开始 | 类似注解但执行机制不同 |
| PY-05 | with | memory / client / file | 理解上下文管理器 | 未开始 | 类似 try-with-resources |
| PY-06 | async/await | MCP / async invoke | 能读懂异步调用 | 未开始 | 对比 CompletableFuture 但语法不同 |
| PY-07 | list/dict comprehension | 数据处理 | 能读懂简洁表达式 | 未开始 | 不必一开始强记 |
| PY-08 | pytest | eval / tests | 能写最小测试 | 未开始 | 后续项目化需要 |

## 9. 学习记录规范

每完成一个知识点，至少更新：

```text
- 知识点总表：状态、开始时间、完成时间、备注
- notes/ 对应笔记：本节总结、关键 API、常见坑
- examples/ 对应代码：可运行
- Git：一次有意义的 commit
```

备注只记录阻塞、偏差、关键决策和下次动作，不复述正文。

## 10. 完成标准

| 层级 | 标准 |
| --- | --- |
| 入门完成 | LC-00 到 LC-06 已完成 |
| 主线完成 | LC-00 到 LC-17 已完成 |
| 进阶完成 | LC-18 到 LC-20 至少完成 2 项 |
| 可项目化 | 能独立搭建 agent + tools + RAG + MCP + LangSmith trace/eval |

## 11. 变更记录

| 时间 | 变更内容 | 影响范围 |
| --- | --- | --- |
| 2026-06-12 | 生成 LangChain 系统学习计划初版 | 全文 |
| 2026-06-13 | 1. 将计划正文迁移到 `.agents/`，并明确 agent 优先读取该文件。<br>2. 将依赖策略调整为使用 PyPI 最新精确版本。<br>3. 将 LangChain 基线从 v1 改为 v1 体系并锁定 `langchain==1.3.9`。<br>4. 明确本项目中的代码注释、Git 提交信息等优先使用中文。 | 文件用途、建议项目结构、环境与命令、LC-00、元信息、执行说明 |
