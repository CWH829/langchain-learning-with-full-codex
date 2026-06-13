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

# 运行示例占位脚本
uv run python examples/01_hello_agent.py
```

当前 `examples/` 中的脚本是按学习路线预留的占位示例，会在对应知识点推进时逐步补全为可运行实现。

## 目录结构

```text
.
├── AGENTS.md
├── .agents/
│   └── LANGCHAIN_PLAN.md
├── deep-research-report.md
├── examples/
├── notes/
├── src/
│   └── langchain_study/
├── tests/
├── .env.example
└── pyproject.toml
```

## 学习推进

学习任务以 `.agents/LANGCHAIN_PLAN.md` 为准。推进某个知识点时，优先核对官方文档，再补充中文讲解、笔记、示例代码和必要测试；完成后更新学习计划中的状态和备注。
