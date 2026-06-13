# LangChain Learning

这是一个面向 Java 开发者的 LangChain v1 学习项目。学习节奏以
`.agents/LANGCHAIN_PLAN.md` 为准：每次推进一个知识点，配套中文笔记、可运行示例和必要测试。

## 当前状态

- 学习计划：`.agents/LANGCHAIN_PLAN.md`
- 主语言：Python
- 项目布局：`src/` layout
- 依赖管理：推荐 `uv`

## 环境准备

如果已经安装 `uv`：

```bash
uv sync
```

如果需要创建或更新依赖：

```bash
uv add langchain langgraph langchain-mcp-adapters
```

本项目暂不固定模型 provider 和 API key。等学习到具体 agent、RAG、MCP 或 LangSmith
任务时，再按需加入 OpenAI、Anthropic、DashScope 等集成包和环境变量。

## 目录结构

```text
.
├── LANGCHAIN_PLAN.md
├── .agents/
│   └── LANGCHAIN_PLAN.md
├── README.md
├── pyproject.toml
├── src/
│   └── langchain_study/
├── examples/
├── notes/
├── data/
└── tests/
```

## 常用命令

```bash
# 同步依赖
uv sync

# 运行一个示例
uv run python examples/01_hello_agent.py

# 运行测试
uv run pytest
```

## 学习推进

每完成一个知识点，至少更新：

- `.agents/LANGCHAIN_PLAN.md` 中对应任务的状态和时间
- `notes/` 中的学习笔记
- `examples/` 中的可运行代码
- 一条有意义的 Git 提交记录
