# LangChain Learning

面向 Java 开发者的 LangChain v1 学习仓库。这个项目用 Python 代码、中文笔记和 Git 记录来系统推进 LangChain、LangGraph、RAG、MCP、LangSmith tracing/evaluation 等主题。

## 文档入口

- `.agents/LANGCHAIN_PLAN.md`：学习路线、当前进度、知识点表和执行说明。
- `.agents/STAGE_SUMMARIES.md`：各阶段轻量摘要，用于按需恢复上下文。
- `.agents/CHANGE_LOG.md`：学习计划变更记录，仅用于追溯计划演进。
- `AGENTS.md`：Codex 协作约束，主要约定代码注释和 Git 提交信息尽量使用中文。
- `deep-research-report.md`：学习计划形成前的资料调研与设计依据。

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

## 目录结构

```text
.
├── AGENTS.md                    # Codex 协作约束
├── .agents/
│   ├── LANGCHAIN_PLAN.md        # LangChain 学习路线和进度记录
│   ├── STAGE_SUMMARIES.md       # 阶段摘要
│   └── CHANGE_LOG.md             # 计划变更记录
├── deep-research-report.md      # 学习计划形成前的资料调研
├── learning/                    # 阶段学习材料（包括代码、知识点文档、笔记等）
│   ├── LC_01_version_boundary/  # LC-01：版本边界
│   ├── LC_02_minimal_agent/     # LC-02：最小 agent
│   └── .....
├── src/
│   └── langchain_study/         # 后续可复用的正式项目代码
├── tests/                      
└── pyproject.toml               
```

学习材料按阶段放在 `learning/` 下。每个阶段目录按实际需要收纳代码、笔记、排障记录或数据样例，不强制固定文件模板。

## 学习推进

学习任务以 `.agents/LANGCHAIN_PLAN.md` 为准。推进某个知识点时，优先核对官方文档，再在对应 `learning/` 阶段目录中补充中文讲解、笔记、示例代码和必要排障记录；完成后更新学习计划中的状态和备注。
