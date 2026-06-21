# LangChain 系统学习计划

## 0. 文件用途

本文件是 Codex 项目中的长期学习路线图与状态文件，用于记录 LangChain 学习路线、当前进度和阶段性决策。

## 1. 元信息

| 字段 | 值 |
| --- | --- |
| 计划版本 | v0.1 |
| LangChain 基线 | LangChain v1，当前锁定 `langchain==1.3.9` |
| 主学习语言 | Python |
| 学习者背景 | Java 开发者，Python 基础较薄弱 |
| 项目语境 | Codex project |
| 学习方式 | 问答讲解 + 学习者手写 Python 代码实践 + Codex 整理知识笔记与 Git 记录 |
| 学习时长 | 未指定 |
| 学习深度 | 先达到能独立完成 agent、RAG、MCP、trace/eval 小项目 |
| 更新时间 | 2026-06-16 |

## 2. Codex Agent 执行说明

1. 先读本文件，找到“知识点总表”中第一条状态为 `⬜` 或 `🟡` 的任务。
2. 开始新阶段学习时，必须先提醒学习者确认当前智能程度为“高”，等待学习者回复后再继续；学习结束后补充完善学习文档前，也需要同样提醒并等待确认。
3. 学习每个知识点前，优先检索官方文档，确认 API、包名、导入路径未过时。优先以官网文档为准，Context7 及其他来源仅作为检索索引和补充，不得替代官网检索。
4. 每个知识点不强制套用固定模板，按实际内容灵活推进，通常包括：目标确认、官方核对、概念讲解、手写实践、实践后观察到的结论、排错记录、阶段总结和进度更新。
5. 学习文档生成时应尽量完整、丰富，尽量覆盖该阶段知识点的关键细节和要点，不要有遗漏。
6. 阶段学习文档可按需加入“图解”小节，用 Mermaid 绘制概念关系图、调用流程图、依赖图、生命周期图等；通常只覆盖当前阶段最关键的 1-2 个结构，避免为了画图而画图。
7. 实践任务较复杂时，可用 Mermaid 绘制补充代码结构图，放在“手写实践任务”小节中，作为补全 TODO 前的代码地图。
8. 代码实践以学习者手写为主；Codex 给思路、片段、骨架和提示，尽量覆盖本阶段涉及的关键 API；关键 TODO 附近可提供注释掉的核心代码片段，便于学习者参考后手写；不直接生成完整实现，也不主动执行大量命令或测试验证，以节省时间和 token。
9. 学习过程中遇到问题时，优先引导学习者自行解决，不主动替其执行。
10. 学习内容以 LangChain、LangGraph 和 Python 为主，默认不强行套 Java 视角；如果概念确实适合类比，可在句末用括号简短补充。
11. 讲解或记录英文术语时可以保留原文；如果属于较高级或不直观的词汇，可在后面用中文括号补充翻译，辅助理解，例如：`transient（短暂的）`。
12. 遇到 Python 特殊语法、特色功能或特性时，按实际需要在学习文档或代码注释中简单解释。
13. 创建 Python 手写骨架文件时，可以同步创建一份 origin 副本，用于保留最初始骨架，默认命名为 `<原文件名>.origin.py`。
14. 学习完成后，先检查代码明显问题、可优化处和实践任务覆盖情况；再结合实践，更新学习文档，如知识细节、实践记录、排错记录和总结等；最后在 `.agents/STAGE_SUMMARIES.md` 中总结阶段摘要。
15. 学习计划变化时，只修改必要内容，并在 `.agents/CHANGE_LOG.md` 中追加摘要；变更记录只记录计划本身的变更。

状态列使用 emoji 记录：`⬜` 表示未开始，`🟡` 表示进行中，`✅` 表示已完成，`⏭️` 表示跳过。

所有时间格式规定：`YYYY-MM-DD HH:mm`


## 3. 建议项目结构

```text
.
├── AGENTS.md                         # Codex 协作约束
├── .agents/
│   ├── LANGCHAIN_PLAN.md             # 学习路线、阶段状态和执行说明
│   ├── STAGE_SUMMARIES.md            # 阶段摘要，按需定向读取
│   └── CHANGE_LOG.md                 # 计划变更记录，仅用于审计
├── README.md
├── pyproject.toml
├── src/
│   └── langchain_study/
├── learning/
│   ├── LC_xx_<topic>/                 # LangChain 主线阶段
│   │   ├── <topic>.md                 # 阶段学习文档
│   │   ├── <topic>_skeleton.py        # 学习者手写练习骨架
│   │   └── <topic>_skeleton.origin.py # 初始骨架副本
│   └── PY_xx_<topic>/                 # Python 补充知识
└── tests/
```

`.agents/` 放学习推进相关的 agent 入口文件：`LANGCHAIN_PLAN.md` 记录路线、阶段状态和执行说明；`STAGE_SUMMARIES.md` 记录阶段摘要；`CHANGE_LOG.md` 仅用于追溯计划变更。

`learning/` 按阶段组织学习材料：`LC_xx_*` 放 LangChain 主线阶段，`PY_xx_*` 放 Python 补充知识。目录名使用下划线而不是连字符，便于必要时作为 Python import 路径使用。LangChain 主线阶段目录默认包含一个阶段学习文档、一个手写骨架文件和一个 origin 初始骨架副本；如阶段内容确有需要，可按实际情况补充排障记录、数据样例等其他文件。

## 4. 资料来源与优先级

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

具体执行约束以“Codex Agent 执行说明”为准。

## 5. 知识点总表

| 状态 | ID | 主题 | 知识点 | 最小目标 | 代码实践 | Python 要点 | 开始时间 | 完成时间 | 资源 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | LC-00 | 项目初始化 | uv、项目结构、Git 规则 | 建好学习仓库 | 初始化项目并首次提交 | venv/uv 与 Maven/Gradle 的区别 | 2026-06-13 | 2026-06-13 | R10 | 已创建 uv 兼容项目骨架；计划迁移到 `.agents/`；依赖改为 PyPI 最新精确版本。 |
| ✅ | LC-01 | 版本边界 | LangChain v1、`create_agent`、`langchain-classic` | 识别新旧资料边界 | 对比 v1 与旧教程导入路径 | 包名和导入路径优先查官方 | 2026-06-13 | 2026-06-13 | R3,R4 | 已核对官方 v1 文档；本地 `.venv` 尚未安装依赖，LC-02 前需同步环境。 |
| ✅ | LC-02 | 最小 agent | `create_agent`、model、tools | 跑通最小 agent | 创建能回答问题并调用工具的 agent | 函数、模块、入口脚本 | 2026-06-13 | 2026-06-13 | R5 | 已跑通最小 agent invoke 和工具调用；环境切到 Python 3.12 + uv；因 OpenAI API 额度不足，改用 DeepSeek OpenAI-compatible API，并补充 `langchain-openai` 依赖。 |
| ✅ | LC-03 | Models | chat model、provider、参数 | 能替换模型 provider | 封装可切换 model 配置 | 环境变量、配置读取 | 2026-06-13 | 2026-06-14 | R6 | 已核对官方 Models 与 ChatOpenAI integration 文档；学习者已补全模型配置骨架，使用 `python-dotenv` 加载本地环境变量，并通过 DeepSeek OpenAI-compatible API 成功调用模型获得响应。 |
| ✅ | LC-04 | Messages | system/user/assistant/tool messages、content blocks | 理解模型上下文结构 | 打印并分析 messages 流 | list/dict、对象属性访问 | 2026-06-14 | 2026-06-14 17:20 | R6 | 已补全 message 流分析骨架，能构造 `SystemMessage` / `HumanMessage`，调用模型并观察 `AIMessage` 的 `content`、`text`、`content_blocks`、`usage_metadata` 等字段；阶段文档已补充知识细节和实践复盘。 |
| ✅ | LC-05 | Tools | tool 定义、参数 schema、tool calling | 会写自定义工具 | search + calculator 双工具 agent | docstring、type hints、异常处理 | 2026-06-14 17:42 | 2026-06-15 10:57 | R6 | 学习者已补全 `search_notes` 和 `calculator` 双工具实践，观察了 `model.bind_tools(...)` 的 `tool_calls` 和 `agent.invoke(...)` 的自动工具调用流程；阶段文档已补充实践复盘、关键问题和总结。 |
| ✅ | LC-06 | Structured Output | `response_format`、Pydantic | 返回稳定结构 | 输出 `TaskPlan` / `StudySummary` | Pydantic 数据模型与字段校验 | 2026-06-15 11:48 | 2026-06-15 15:23 | R6 | 学习者已补全 `TaskPlan` 和 `StudySummary` 两套 Pydantic schema，观察了 `response_format=TaskPlan`、`ToolStrategy(StudySummary)`、`structured_response` 与 `model_dump()`；已记录 DeepSeek V4 Pro thinking mode 与 `tool_choice` 冲突，并通过关闭 thinking 解决。 |
| ✅ | LC-07 | Runtime | runtime context、tool runtime | 理解运行期上下文 | 在工具中读取上下文 | 参数注入、可选参数 | 2026-06-15 16:07 | 2026-06-15 19:05 | R6 | 学习者已补全 runtime context 实践，理解 `context_schema`、`agent.invoke(..., context=...)`、工具中的 `ToolRuntime`、`runtime.context` 和 `runtime.state`；已记录 `InvalidUpdateError: Expected dict` 的排错过程。 |
| ✅ | LC-08 | Middleware | middleware、logging、HITL、summarization | 给 agent 加控制逻辑 | 加日志/摘要/人工确认 | 装饰器、函数式组合 | 2026-06-15 19:19 | 2026-06-16 18:39 | R6 | 学习者已补全 logging middleware、HITL 人工确认和 summarization 构造实践；已观察 node-style hooks 的执行时机、`GraphOutput.value` / `GraphOutput.interrupts`、checkpointer + `thread_id` 的作用，并完成阶段文档复盘。 |
| ✅ | LC-09 | 上下文工程 | prompt、tool context、context lifecycle | 控制成本与行为 | 精简 system prompt + 按需加载资料 | 长文本拆分、上下文边界 | 2026-06-16 21:05 | 2026-06-17 14:14 | R6 | 学习者已完成上下文工程实践，观察了 `@dynamic_prompt`、`@wrap_model_call`、`request.override(tools=...)`、`ToolRuntime`、`runtime.context` 和 `runtime.state`；已记录动态 prompt 不进入 `result["messages"]`、`max_materials` 只限制单次工具返回等结论。 |
| ✅ | LC-10 | Short-term Memory | thread-scoped memory、checkpointer | 实现线程内记忆 | 多轮对话保留上下文 | `with`、资源管理 | 2026-06-17 14:28 | 2026-06-17 16:35 | R6 | 学习者已完成 short-term memory 实践，理解 `InMemorySaver`、`checkpointer`、`thread_id`、同线程多轮 messages 追加、不同线程状态隔离，以及 `agent.get_state(config)` 查看 checkpoint state。 |
| ✅ | LC-11 | Long-term Memory | store、跨会话记忆 | 区分短期/长期记忆 | 存取用户偏好示例 | 数据结构、序列化 | 2026-06-17 16:59 | 2026-06-17 21:43 | R6 | 学习者已完成长期记忆实践，理解 `InMemoryStore`、`namespace`、`key`、`runtime.store`、`runtime.context.user_id`，并观察了同一用户跨 thread 读取偏好与不同用户隔离。 |
| ✅ | LC-12 | Retrieval 基础 | documents、splitters、embeddings、vector store | 能做语义检索 | 文本切分 + 向量检索 | 文件读写、列表处理 | 2026-06-17 21:56 | 2026-06-19 11:55 | R6 | 已完成 Retrieval 基础实践；4 个原始 Document 切为 6 个 chunk，确认 metadata 与 `start_index` 保留、180 字符上限、两种检索入口结果一致，并识别关键词 embedding 的零分并列噪声和 NumPy 依赖。 |
| ✅ | LC-13 | 2-step RAG | retrieve -> generate | 做最小知识问答 | 本地文本问答 | pipeline 思维 | 2026-06-19 12:03 | 2026-06-19 17:51 | R6,R11 | 已完成 retrieve、context formatting、单次 model generation 与 sources 回传；已验证两个已知问题和一个未知问题，并记录教学 embedding 全零向量导致 cosine similarity NaN 的排错过程。 |
| ✅ | LC-14 | Agentic / Hybrid RAG | agentic retrieval、query rewrite、validation | 知道何时升级 RAG | 给 agent 增加检索工具 | 控制流、结果校验 | 2026-06-19 18:30 | 2026-06-20 20:44 | R6,R11 | 已完成 Agentic 与 Hybrid RAG 实践；观察 agent 首次中文 query 零命中后自主二次检索，完成 `content_and_artifact` 来源保留、query rewrite、score threshold、semantic grader 和未知问题提前拒答；记录 DeepSeek structured output 需使用 `function_calling`。 |
| ✅ | LC-15 | MCP | MCP、`langchain-mcp-adapters`、docs MCP | 接入外部工具/文档 | 让 agent 调用 MCP server | async/await、客户端生命周期 | 2026-06-21 11:05 | 2026-06-21 16:12 | R1,R2,R6 | 已完成本地 FastMCP stdio server、MultiServerMCPClient、异步 agent 调用和消息流观察；确认 structured content 到 artifact 的转换，并区分业务未命中、tool 执行错误与 transport/session 错误。 |
| ✅ | LC-16 | LangSmith Tracing | tracing、runs、observability | 能定位 agent 行为 | 记录完整 agent trace，并用 `@traceable` 手动埋点 | 环境变量、SDK 配置 | 2026-06-21 16:22 | 2026-06-21 18:36 | R7 | 已完成自动 agent tracing 与 `@traceable` 手动埋点；在 LangSmith UI 中观察 model/tool 调用链、普通函数与 model 的父子 runs，以及自定义和框架内部 tags、metadata、耗时与输入输出。 |
| ⬜ | LC-17 | LangSmith Evaluation | dataset、evaluator、experiment | 做最小离线评测 | 对 RAG/agent 做 mini eval | 测试思维、函数返回结构 |  |  | R8 |  |
| ⬜ | LC-18 | LangGraph 入门 | graph、state、node、edge | 理解何时用 LangGraph | Router 或简单 workflow | TypedDict、状态传递 |  |  | R9 |  |
| ⬜ | LC-19 | Multi-agent | supervisor、handoff、subagent | 了解多 agent 设计边界 | 可选 subagent demo | 上下文隔离 |  |  | R6,R9 | 可选 |
| ⬜ | LC-20 | 综合小项目 | agent + tools + RAG + MCP + tracing/eval | 完成可复盘项目 | 做一个个人知识库问答 agent | 项目组织、测试、提交 |  |  | R1-R9 |  |

## 6. Python 补充学习索引

| 状态 | ID | 主题 | 触发场景 | 学习目标 | 备注 |
| --- | --- | --- | --- | --- | --- |
| ✅ | PY-01 | venv / uv | 初始化项目、LC-02 环境排障 | 理解 Python 依赖隔离 | 已整理 `learning/PY_01_venv_uv/venv_uv.md`；LC-00 阶段完成 uv/venv 基础概念，LC-02 阶段实际解决 uv 安装、Python 3.12 虚拟环境、依赖同步和 PyCharm 解释器配置问题。 |
| ✅ | PY-02 | type hints | 写 tools / schema | 能读写常见类型标注 | 已在 LC-05 Tools 中掌握函数参数和返回值类型标注，并理解 type hints 会影响工具 schema，但不等于 Python 运行时校验；LC-06 中继续使用 `Literal`、`list[str]`、<code>str &#124; None</code> 等常见类型标注。 |
| ✅ | PY-03 | Pydantic / dataclass | structured output | 会定义轻量数据模型 | 已在 LC-03 接触 dataclass 配置对象，在 LC-06 完成 Pydantic `BaseModel`、`Field(...)`、`Literal`、`ValidationError` 思路和 `model_dump()` 序列化基础。 |
| ✅ | PY-04 | decorators | tool / middleware | 理解装饰器包装函数 | 已在 LC-08 中结合 `@tool`、middleware hook 和 Java AOP 类比，理解装饰器用于包装/注册函数，以及框架按约定调用被注册函数的基本思路。 |
| ✅ | PY-05 | with | memory / client / file | 理解上下文管理器 | 已在 LC-10 中结合数据库型 checkpointer 场景理解 `with ... as ...` 的资源进入、退出和异常清理作用。 |
| ⬜ | PY-06 | async/await | MCP / async invoke | 能读懂异步调用 | 关注事件循环、协程和异步资源生命周期 |
| ⬜ | PY-07 | list/dict comprehension | 数据处理 | 能读懂简洁表达式 | 不必一开始强记 |
| ⬜ | PY-08 | pytest | eval / tests | 能写最小测试 | 后续项目化需要 |

## 7. 学习记录规范

学习记录只记录有复盘价值的信息。每完成或阶段性推进一个知识点时，按实际情况更新：

- 知识点总表：状态、开始时间、完成时间、关键备注
- `.agents/STAGE_SUMMARIES.md` 阶段摘要记录表：按阶段记录核心结论、关键 API / 概念、后续依赖
- `learning/` 对应阶段目录：学习文档、手写骨架、origin 副本
- 学习文档：记录完整知识细节、图解、实践记录、观察结果、核心结论、阶段总结等
- 备注：只记录阻塞、偏差、关键决策和下次动作，不复述正文
- Git：完成阶段性改动后，记录本次改动摘要，并只提供建议提交信息

## 8. 完成标准

| 层级 | 标准 |
| --- | --- |
| 入门完成 | LC-00 到 LC-06 已完成 |
| 主线完成 | LC-00 到 LC-17 已完成 |
| 进阶完成 | LC-18 到 LC-20 至少完成 2 项 |
| 可项目化 | 能独立搭建 agent + tools + RAG + MCP + LangSmith trace/eval |
