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
| 更新时间 | 2026-06-13 |

## 2. Codex Agent 执行说明

1. 先读本文件，找到“知识点总表”中第一条状态为“未开始”或“进行中”的任务。
2. 开始新阶段学习时，必须先提醒学习者确认当前智能程度为“高”，等待学习者回复后再继续执行；学习结束后补充完善学习文档前，也需要同样提醒并等待确认。
3. 学习每个知识点前，优先检索官方文档，确认 API、包名、导入路径未过时。
4. 每个知识点按实际内容灵活推进，可参考这些动作规划：官方核对、概念讲解、整理知识笔记、引导代码实践、排错记录、阶段总结、进度更新等。
5. 学习文档生成时应尽量完整、丰富，尽量覆盖当前知识点的关键细节和要点；文档结构和写法可按当前知识点灵活调整，不必严格沿用上一阶段文档风格和结构，适当参考即可；
6. 学习完成后，先检查一下代码情况，有没有问题以及可以优化的地方；然后可结合实践结果继续补充完善，如知识细节、实践记录、排错记录和总结等。
7. 代码以 Python 为主；遇到 Python 特殊语法、特色功能、特性等内容时，按实际需要在学习文档或代码注释中简单解释。
8. 代码实践以学习者手写为主；Codex 给思路、片段、骨架和提示，不直接生成完整实现 然后执行各种命令 做各种测试验证等等，否则既耗时又耗token额度。
9. 创建 Python 手写骨架文件时，可以同步创建一份 origin 副本，用于保留最初始骨架，默认命名为 `<原文件名>.origin.py`。
10. 学习过程中遇到问题时，优先引导学习者自行解决，不主动替其执行。
11. 学习计划变化时，只修改必要内容，并在“变更记录”中追加摘要；注意，该表只记录计划本身的变更。
12. 为节省 token，不要一次性展开所有知识点；只展开当前任务需要的资料、概念和必要代码片段。

状态列使用 emoji 记录：`⬜` 表示未开始，`🟡` 表示进行中，`✅` 表示已完成，`⏭️` 表示跳过。

所有时间格式规定：`YYYY-MM-DD HH:mm`

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
├── AGENTS.md                         # Codex 协作约束
├── .agents/
│   └── LANGCHAIN_PLAN.md             # 完整学习计划
├── README.md
├── pyproject.toml
├── src/
│   └── langchain_study/
├── learning/
│   ├── LC_01_version_boundary/
│   │   └── version_boundary.md
│   ├── LC_02_minimal_agent/
│   │   ├── hello_agent.py
│   │   └── minimal_agent.md
│   ├── LC_03_models/
│   │   ├── model_config_skeleton.py
│   │   ├── model_config_skeleton.origin.py
│   │   └── models.md
│   └── PY_01_venv_uv/
│       └── venv_uv.md
└── tests/
```

`learning/` 按阶段组织学习材料：`LC_xx_*` 放 LangChain 主线阶段，`PY_xx_*` 放 Python 补充知识。目录名使用下划线而不是连字符，便于必要时作为 Python import 路径使用。每个阶段目录不强制固定文件名或文件数量，按实际学习内容放置代码、笔记、排障记录、数据样例等。

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

每个知识点不强制套用固定模板，可按实际内容参考以下节奏：

```text
1. 明确当前知识点目标
2. 核对官方资料
3. 讲清关键概念并整理学习文档
4. 给出手写实践目标、步骤、片段或骨架
5. 引导排错并记录有价值的问题
6. 学习结束后补充知识细节、实践记录和总结
7. 更新学习计划进度
```

具体执行约束以“Codex Agent 执行说明”为准。

## 7. 知识点总表

| 状态 | ID | 主题 | 知识点 | 最小目标 | 产出 | 代码实践 | Python 要点 | 开始时间 | 完成时间 | 资源 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | LC-00 | 项目初始化 | uv、项目结构、Git 规则 | 建好学习仓库 | 初始目录 + README | 初始化项目并首次提交 | venv/uv 与 Maven/Gradle 的区别 | 2026-06-13 | 2026-06-13 | R10 | 已创建 uv 兼容项目骨架；计划迁移到 `.agents/`；依赖改为 PyPI 最新精确版本。 |
| ✅ | LC-01 | 版本边界 | LangChain v1、`create_agent`、`langchain-classic` | 识别新旧资料边界 | `learning/LC_01_version_boundary/version_boundary.md` | 对比 v1 与旧教程导入路径 | 包名和导入路径优先查官方 | 2026-06-13 | 2026-06-13 | R3,R4 | 已核对官方 v1 文档；本地 `.venv` 尚未安装依赖，LC-02 前需同步环境。 |
| ✅ | LC-02 | 最小 agent | `create_agent`、model、tools | 跑通最小 agent | `learning/LC_02_minimal_agent/hello_agent.py`、`learning/LC_02_minimal_agent/minimal_agent.md` | 创建能回答问题并调用工具的 agent | 函数、模块、入口脚本 | 2026-06-13 | 2026-06-13 | R5 | 已跑通最小 agent invoke 和工具调用；环境切到 Python 3.12 + uv；因 OpenAI API 额度不足，改用 DeepSeek OpenAI-compatible API，并补充 `langchain-openai` 依赖。 |
| ✅ | LC-03 | Models | chat model、provider、参数 | 能替换模型 provider | `learning/LC_03_models/models.md`、`learning/LC_03_models/model_config_skeleton.py` | 封装可切换 model 配置 | 环境变量、配置读取 | 2026-06-13 | 2026-06-14 | R6 | 已核对官方 Models 与 ChatOpenAI integration 文档；学习者已补全模型配置骨架，使用 `python-dotenv` 加载本地环境变量，并通过 DeepSeek OpenAI-compatible API 成功调用模型获得响应。 |
| ✅ | LC-04 | Messages | system/user/assistant/tool messages、content blocks | 理解模型上下文结构 | `learning/LC_04_messages/messages.md`、`learning/LC_04_messages/message_flow_skeleton.py` | 打印并分析 messages 流 | list/dict、对象属性访问 | 2026-06-14 | 2026-06-14 17:20 | R6 | 已补全 message 流分析骨架，能构造 `SystemMessage` / `HumanMessage`，调用模型并观察 `AIMessage` 的 `content`、`text`、`content_blocks`、`usage_metadata` 等字段；阶段文档已补充知识细节和实践复盘。 |
| ✅ | LC-05 | Tools | tool 定义、参数 schema、tool calling | 会写自定义工具 | `learning/LC_05_tools/tools.md`、`learning/LC_05_tools/tool_calling_skeleton.py` | search + calculator 双工具 agent | docstring、type hints、异常处理 | 2026-06-14 17:42 | 2026-06-15 10:57 | R6 | 学习者已补全 `search_notes` 和 `calculator` 双工具实践，观察了 `model.bind_tools(...)` 的 `tool_calls` 和 `agent.invoke(...)` 的自动工具调用流程；阶段文档已补充实践复盘、关键问题和总结。 |
| ✅ | LC-06 | Structured Output | `response_format`、Pydantic | 返回稳定结构 | `learning/LC_06_structured_output/structured_output.md`、`learning/LC_06_structured_output/structured_output_skeleton.py` | 输出 `TaskPlan` / `StudySummary` | Pydantic 数据模型与字段校验 | 2026-06-15 11:48 | 2026-06-15 15:23 | R6 | 学习者已补全 `TaskPlan` 和 `StudySummary` 两套 Pydantic schema，观察了 `response_format=TaskPlan`、`ToolStrategy(StudySummary)`、`structured_response` 与 `model_dump()`；已记录 DeepSeek V4 Pro thinking mode 与 `tool_choice` 冲突，并通过关闭 thinking 解决。 |
| ⬜ | LC-07 | Runtime | runtime context、tool runtime | 理解运行期上下文 |  | 在工具中读取上下文 | 参数注入、可选参数 |  |  | R6 |  |
| ⬜ | LC-08 | Middleware | middleware、logging、HITL、summarization | 给 agent 加控制逻辑 |  | 加日志/摘要/人工确认 | 装饰器、函数式组合 |  |  | R6 |  |
| ⬜ | LC-09 | 上下文工程 | prompt、tool context、context lifecycle | 控制成本与行为 |  | 精简 system prompt + 按需加载资料 | 长文本拆分、上下文边界 |  |  | R6 |  |
| ⬜ | LC-10 | Short-term Memory | thread-scoped memory、checkpointer | 实现线程内记忆 |  | 多轮对话保留上下文 | `with`、资源管理 |  |  | R6 |  |
| ⬜ | LC-11 | Long-term Memory | store、跨会话记忆 | 区分短期/长期记忆 |  | 存取用户偏好示例 | 数据结构、序列化 |  |  | R6 |  |
| ⬜ | LC-12 | Retrieval 基础 | documents、splitters、embeddings、vector store | 能做语义检索 |  | 文本切分 + 向量检索 | 文件读写、列表处理 |  |  | R6 |  |
| ⬜ | LC-13 | 2-step RAG | retrieve -> generate | 做最小知识问答 |  | 本地文本问答 | pipeline 思维 |  |  | R6,R11 |  |
| ⬜ | LC-14 | Agentic / Hybrid RAG | agentic retrieval、query rewrite、validation | 知道何时升级 RAG |  | 给 agent 增加检索工具 | 控制流、结果校验 |  |  | R6,R11 |  |
| ⬜ | LC-15 | MCP | MCP、`langchain-mcp-adapters`、docs MCP | 接入外部工具/文档 |  | 让 agent 调用 MCP server | async/await、客户端生命周期 |  |  | R1,R2,R6 |  |
| ⬜ | LC-16 | LangSmith Tracing | tracing、runs、observability | 能定位 agent 行为 |  | 记录一次完整 agent trace | 环境变量、SDK 配置 |  |  | R7 |  |
| ⬜ | LC-17 | LangSmith Evaluation | dataset、evaluator、experiment | 做最小离线评测 |  | 对 RAG/agent 做 mini eval | 测试思维、函数返回结构 |  |  | R8 |  |
| ⬜ | LC-18 | LangGraph 入门 | graph、state、node、edge | 理解何时用 LangGraph |  | Router 或简单 workflow | TypedDict、状态传递 |  |  | R9 |  |
| ⬜ | LC-19 | Multi-agent | supervisor、handoff、subagent | 了解多 agent 设计边界 |  | 可选 subagent demo | 上下文隔离 |  |  | R6,R9 | 可选 |
| ⬜ | LC-20 | 综合小项目 | agent + tools + RAG + MCP + tracing/eval | 完成可复盘项目 |  | 做一个个人知识库问答 agent | 项目组织、测试、提交 |  |  | R1-R9 |  |

## 8. Python 补充学习索引

| 状态 | ID | 主题 | 触发场景 | 学习目标 | 备注 |
| --- | --- | --- | --- | --- | --- |
| ✅ | PY-01 | venv / uv | 初始化项目、LC-02 环境排障 | 理解 Python 依赖隔离 | 已整理 `learning/PY_01_venv_uv/venv_uv.md`；LC-00 阶段完成 uv/venv 基础概念，LC-02 阶段实际解决 uv 安装、Python 3.12 虚拟环境、依赖同步和 PyCharm 解释器配置问题。 |
| ✅ | PY-02 | type hints | 写 tools / schema | 能读写常见类型标注 | 已在 LC-05 Tools 中掌握函数参数和返回值类型标注，并理解 type hints 会影响工具 schema，但不等于 Python 运行时校验；LC-06 中继续使用 `Literal`、`list[str]`、`str | None` 等常见类型标注。 |
| ✅ | PY-03 | Pydantic / dataclass | structured output | 会定义轻量数据模型 | 已在 LC-03 接触 dataclass 配置对象，在 LC-06 完成 Pydantic `BaseModel`、`Field(...)`、`Literal`、`ValidationError` 思路和 `model_dump()` 序列化基础。 |
| ⬜ | PY-04 | decorators | tool / middleware | 理解装饰器包装函数 | 关注函数包装、注册和调用时机 |
| ⬜ | PY-05 | with | memory / client / file | 理解上下文管理器 | 关注资源进入、退出和异常清理 |
| ⬜ | PY-06 | async/await | MCP / async invoke | 能读懂异步调用 | 关注事件循环、协程和异步资源生命周期 |
| ⬜ | PY-07 | list/dict comprehension | 数据处理 | 能读懂简洁表达式 | 不必一开始强记 |
| ⬜ | PY-08 | pytest | eval / tests | 能写最小测试 | 后续项目化需要 |

## 9. 学习记录规范

学习记录只记录有复盘价值的信息，执行规则以第 2 节和第 6 节为准。每完成或阶段性推进一个知识点时，按实际情况更新：

```text
- 知识点总表：状态、开始时间、完成时间、产出路径、关键备注
- `learning/` 对应阶段目录：学习文档、手写骨架、origin 副本、实践记录、排错记录、阶段总结等
- 学习文档：尽量沉淀为可复习材料，覆盖核心概念、关键 API、字段/参数细节、常见坑和实践结论等
- 备注：只记录阻塞、偏差、关键决策和下次动作，不复述正文
- Git：完成阶段性改动后，记录本次改动摘要，并只提供建议提交信息
```

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
| 2026-06-13 | 1. 迁移完整计划到 `.agents/LANGCHAIN_PLAN.md`。<br>2. 锁定 LangChain v1 相关依赖版本。<br>3. 调整建议项目结构，移除根目录 `LANGCHAIN_PLAN.md` 入口文件。<br>4. 将代码注释、Git 提交信息等协作约束收敛到根目录 `AGENTS.md`。 | 文件用途、元信息、环境与命令、建议项目结构、执行说明、LC-00 |
| 2026-06-13 | 调整学习推进方式：必要动作保留，输出形式按知识点灵活安排；练习题、小任务、常见坑等改为按需补充。 | 执行说明、学习推进协议、学习记录规范 |
| 2026-06-13 | 调整协作方式：代码实践改为学习者手写为主，Codex 负责讲解、知识笔记、骨架提示、排错引导和进度记录；默认不代写完整实现、不主动跑测试。 | 元信息、执行说明、学习推进协议、学习记录规范、LC-02 |
| 2026-06-13 | 知识点总表状态列移到最前，改用 Windows emoji 记录；完成状态要求达到知识点目标或学习者明确表示学完，不能刚开始就标完成。 | 执行说明、知识点总表、学习记录规范 |
| 2026-06-13 | Git 提交流程改为 Codex 只提供建议提交信息，学习者自行审核并手动提交。 | 学习记录规范 |
| 2026-06-13 | 增加手动处理原则：有学习价值的环境、依赖、软件安装、参数和环境变量配置问题，由 Codex 引导学习者手动解决。 | 执行说明、协作约束 |
| 2026-06-13 | 项目学习材料改为按阶段目录组织：`learning/LC-xx_*` 和 `learning/PY-xx_*` 收纳对应阶段的代码、笔记和排障记录，不再按 `examples/`、`notes/` 类型拆分。 | 建议项目结构、知识点总表、Python 补充学习索引、学习记录规范 |
| 2026-06-13 | 细化阶段推进与记录规则：学习后需要补充实践记录或总结；未开始阶段不提前固定产出文件；Python 补充学习索引状态列改用与知识点总表一致的 emoji。 | 执行说明、知识点总表、Python 补充学习索引 |
| 2026-06-13 | 调整 Git 记录规范表述：提供建议提交信息和改动摘要，学习者自行手动提交。 | 学习记录规范 |
| 2026-06-13 | 增加新阶段启动前确认规则：涉及资料检索、官方文档核对、知识点整理、文件生成等操作前，Codex 先提醒学习者确认智能程度为“高”，等待回复后再继续。 | 执行说明、协作约束 |
| 2026-06-13 | 增加 Python 手写骨架 origin 副本规则：创建骨架文件时可同步保留最初始副本，便于未来复用或对照。 | 执行说明、协作约束 |
| 2026-06-14 | 调整 `learning/` 阶段目录命名：将 `LC-xx_*`、`PY-xx_*` 改为 `LC_xx_*`、`PY_xx_*`，避免连字符影响 Python import。 | 建议项目结构、知识点总表、Python 补充学习索引 |
| 2026-06-14 | 1. 取消默认 Java 视角类比，后续讲解聚焦 LangChain 与 Python 学习主题本身。<br>2. 明确阶段文档策略：生成时尽量完整、丰富，覆盖当前知识点关键细节；阶段完成后结合实践继续补全为可复习的完整知识文档，而不只是追加实践记录或总结。<br>3. 学习推进动作改为参考项，由 Codex 按实际内容灵活判断和规划。 | 元信息、执行说明、学习推进协议、Python 补充学习索引、学习记录规范 |
| 2026-06-14 | 补充智能程度确认规则：学习结束后补充完善学习文档前，也需要提醒学习者确认当前智能程度为“高”并等待回复。 | 执行说明 |
| 2026-06-14 | 按新版执行说明调整“学习推进协议”：补充阶段开始和学习结束补文档前的智能程度确认，强调文档完整性、Python 按需解释、手写实践和排错引导。 | 学习推进协议 |
| 2026-06-14 | 简化“学习推进协议”：第 2 节保留硬性执行约束，第 6 节只保留知识点推进节奏，避免两处重复维护同一套规则。 | 学习推进协议 |
| 2026-06-14 | 调整“学习记录规范”：聚焦记录内容和复盘价值，不再重复代码实践、测试验证等执行约束。 | 学习记录规范 |
| 2026-06-14 17:58 | 补充学习文档生成规则：阶段文档不必严格沿用上一阶段风格和结构，可按当前知识点灵活调整，适当参考即可。 | 执行说明 |
