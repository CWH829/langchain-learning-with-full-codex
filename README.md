# LangChain Learning

面向 Java 开发者的 LangChain v1 学习仓库。这个项目用 Python 代码、中文笔记和 Git 记录来系统推进 LangChain、LangGraph、RAG、MCP、LangSmith tracing/evaluation 等主题。

## 文档入口

- `.agents/LANGCHAIN_PLAN.md`：学习路线、当前进度、知识点表和执行说明。
- `.agents/STAGE_SUMMARIES.md`：各阶段轻量摘要，用于按需恢复上下文。
- `.agents/CHANGE_LOG.md`：学习计划变更记录，仅用于追溯计划演进。
- `AGENTS.md`：Codex 协作约束，主要约定代码注释和 Git 提交信息尽量使用中文。
- `deep-research-report.md`：学习计划形成前的资料调研与设计依据。

## 目录结构

```text
.
├── .agents/                              
│   ├── LANGCHAIN_PLAN.md                 # 核心文件：学习计划文档
│   ├── STAGE_SUMMARIES.md                # 已完成阶段的轻量摘要
│   └── CHANGE_LOG.md                     # 学习计划变更记录
├── learning/                             
│   ├── PY_01_venv_uv/                    # Python 虚拟环境与 uv
│   ├── LC_01_version_boundary/           # LangChain v1 版本边界
│   ├── LC_02_minimal_agent/              # 最小 agent 学习笔记
│   ├── LC_03_models/                     # Models
│   ├── LC_04_messages/                   # Messages
│   ├── LC_05_tools/                      # Tools
│   ├── LC_06_structured_output/          # Structured Output
│   ├── LC_07_runtime/                    # Runtime
│   ├── LC_08_middleware/                 # Middleware
│   ├── LC_09_context_engineering/        # 上下文工程
│   ├── LC_10_short_term_memory/          # 短期记忆
│   ├── LC_11_long_term_memory/           # 长期记忆
│   ├── LC_12_retrieval_basics/           # Retrieval 基础
│   ├── LC_13_two_step_rag/                # 2-step RAG
│   ├── LC_14_agentic_hybrid_rag/          # Agentic / Hybrid RAG
│   ├── LC_15_mcp/                         # MCP
│   ├── LC_16_langsmith_tracing/           # LangSmith Tracing
│   ├── LC_17_langsmith_evaluation/        # LangSmith Evaluation
│   └── .....                              # 后续阶段待开发
├── src/
│   └── langchain_study/                  # 可复用的正式项目代码
├── tests/
│   └── test_project_import.py            
├── .env                                  # 本地环境变量，不提交真实密钥
├── .gitignore                            
├── AGENTS.md                             # Codex 约束
├── deep-research-report.md               # 学习计划的前期资料调研
├── pyproject.toml                        
├── uv.lock                               
└── README.md                                                           
```

## 学习阶段

`learning/` 按知识点拆分为递进阶段。每个 LangChain 阶段通常包含中文学习笔记、手写练习骨架和初始骨架副本。

| 阶段 | 主题 | 学习重点 | 学习笔记 |
| --- | --- | --- | --- |
| PY-01 | venv / uv | Python 虚拟环境、`uv` 项目与依赖管理 | [venv_uv.md](learning/PY_01_venv_uv/venv_uv.md) |
| LC-01 | 版本边界 | 确认 LangChain v1 的版本范围、包职责与官方资料入口 | [version_boundary.md](learning/LC_01_version_boundary/version_boundary.md) |
| LC-02 | 最小 Agent | 使用 `create_agent` 构建并运行最小可用 agent | [minimal_agent.md](learning/LC_02_minimal_agent/minimal_agent.md) |
| LC-03 | Models | 模型初始化、参数配置、调用方式与 provider 接入 | [models.md](learning/LC_03_models/models.md) |
| LC-04 | Messages | 消息类型、消息内容、对话历史与消息流转 | [messages.md](learning/LC_04_messages/messages.md) |
| LC-05 | Tools | 工具定义、参数 schema、tool calling 与执行结果回传 | [tools.md](learning/LC_05_tools/tools.md) |
| LC-06 | Structured Output | 使用 schema 约束模型输出并获得结构化结果 | [structured_output.md](learning/LC_06_structured_output/structured_output.md) |
| LC-07 | Runtime | 运行时上下文、依赖注入以及 tool 中的上下文访问 | [runtime.md](learning/LC_07_runtime/runtime.md) |
| LC-08 | Middleware | agent 中间件、生命周期钩子与行为扩展 | [middleware.md](learning/LC_08_middleware/middleware.md) |
| LC-09 | 上下文工程 | 根据任务选择、组织和控制进入模型的上下文 | [context_engineering.md](learning/LC_09_context_engineering/context_engineering.md) |
| LC-10 | Short-term Memory | 基于 thread 与 checkpointer 管理单次会话记忆 | [short_term_memory.md](learning/LC_10_short_term_memory/short_term_memory.md) |
| LC-11 | Long-term Memory | 跨会话持久化、命名空间与长期记忆读写 | [long_term_memory.md](learning/LC_11_long_term_memory/long_term_memory.md) |
| LC-12 | Retrieval 基础 | Document、文本切分、embedding、vector store 与 retriever | [retrieval_basics.md](learning/LC_12_retrieval_basics/retrieval_basics.md) |
| LC-13 | 2-step RAG | 固定执行 retrieve、context formatting 与单次 generation | [two_step_rag.md](learning/LC_13_two_step_rag/two_step_rag.md) |
| LC-14 | Agentic / Hybrid RAG | agentic retrieval、query rewrite、结果校验与混合控制流 | [agentic_hybrid_rag.md](learning/LC_14_agentic_hybrid_rag/agentic_hybrid_rag.md) |
| LC-15 | MCP | FastMCP、stdio、MCP client、异步工具加载与 agent 调用 | [mcp.md](learning/LC_15_mcp/mcp.md) |
| LC-16 | LangSmith Tracing | 自动 tracing、手动埋点、run tree 与调用链观察 | [langsmith_tracing.md](learning/LC_16_langsmith_tracing/langsmith_tracing.md) |
| LC-17 | LangSmith Evaluation | dataset、target function、evaluator 与 experiment | [langsmith_evaluation.md](learning/LC_17_langsmith_evaluation/langsmith_evaluation.md) |


## 当前基线

- Python：`>=3.11`
- LangChain：`langchain==1.3.9`
- LangGraph：`langgraph==1.2.5`
- MCP 适配：`langchain-mcp-adapters==0.3.0`
- OpenAI-compatible 模型接入：`langchain-openai`
- 本地环境变量加载：`python-dotenv`
- 测试与检查：`pytest==9.0.3`、`ruff==0.15.17`

依赖版本以 `pyproject.toml` 和 `uv.lock` 为准。模型 provider、API key 和额外集成包不在初始化阶段固定；学习到具体 agent、RAG、MCP 或 LangSmith 任务时再按需加入。

## 环境与命令

本项目推荐使用 `uv` 管理 Python 虚拟环境和依赖。

已有仓库的日常同步命令：

```bash
uv sync
```

常用检查命令按需执行：

```bash
uv run pytest
uv run ruff check .
```

如需重新创建类似项目，可参考以下初始化命令：

```bash
uv init
uv add langchain==1.3.9 langgraph==1.2.5 langchain-mcp-adapters==0.3.0
uv add langchain-openai python-dotenv
uv add --dev pytest==9.0.3 ruff==0.15.17
```

如需接入 LangChain 官方文档 MCP，可在 Codex 环境中配置：

```bash
codex mcp add langchain-docs --url https://docs.langchain.com/mcp
```

模型 provider、API key、LangSmith key 等本地配置按当前学习任务补充到 `.env` 或系统环境变量中。不要把真实密钥提交到 Git。

## 学习推进

学习任务以 `.agents/LANGCHAIN_PLAN.md` 为准。推进某个知识点时，优先核对官方文档，再在对应 `learning/` 阶段目录中补充中文讲解、笔记、示例代码和必要排障记录；完成后更新学习计划中的状态和备注。
