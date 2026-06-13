# LangChain Learning

面向 Java 开发者的 LangChain v1 学习仓库。这个项目用 Python 代码、中文笔记和 Git 记录来系统推进 LangChain、LangGraph、RAG、MCP、LangSmith tracing/evaluation 等主题。

## 文档入口

- `.agents/LANGCHAIN_PLAN.md`：完整学习路线、当前进度、知识点表和执行说明。
- `AGENTS.md`：Codex 协作约束，主要约定代码注释和 Git 提交信息尽量使用中文。
- `deep-research-report.md`：学习计划形成前的资料调研与设计依据。

## 当前基线

- Python：`>=3.11`
- LangChain：`langchain==1.3.9`
- LangGraph：`langgraph==1.2.5`
- MCP 适配：`langchain-mcp-adapters==0.3.0`
- 测试与检查：`pytest`、`ruff`

模型 provider、API key 和额外集成包不在初始化阶段固定；学习到具体 agent、RAG、MCP 或 LangSmith 任务时再按需加入。

## 环境准备

推荐使用 `uv`：

```bash
uv sync
```

如需配置模型或 LangSmith key，可从 `.env.example` 复制并按当前学习任务补充。

## 常用命令

```bash
# 运行测试
uv run pytest

# 运行 ruff 检查
uv run ruff check .

# 运行 LC-02 最小 agent 示例
uv run python learning/LC-02_minimal_agent/hello_agent.py
```

学习材料按阶段放在 `learning/` 下。每个阶段目录按实际需要收纳代码、笔记、排障记录或数据样例，不强制固定文件模板。

## 目录结构

```text
.
├── AGENTS.md
├── .agents/
│   └── LANGCHAIN_PLAN.md
├── deep-research-report.md
├── learning/
│   ├── LC-01_version_boundary/
│   ├── LC-02_minimal_agent/
│   └── PY-01_venv_uv/
├── src/
│   └── langchain_study/
├── tests/
├── .env.example
└── pyproject.toml
```

## 学习推进

学习任务以 `.agents/LANGCHAIN_PLAN.md` 为准。推进某个知识点时，优先核对官方文档，再在对应 `learning/` 阶段目录中补充中文讲解、笔记、示例代码和必要排障记录；完成后更新学习计划中的状态和备注。
