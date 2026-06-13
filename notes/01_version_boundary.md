# LC-01 版本边界

## 当前知识点目标

学会判断一份 LangChain 教程、示例或代码片段是不是适用于当前仓库的 LangChain v1 学习路线。重点不是背 API，而是形成一个检查习惯：先确认包名、导入路径和推荐入口，再动手写代码。

## 官方资料确认

- LangChain v1 发布说明：<https://docs.langchain.com/oss/python/releases/langchain-v1>
- LangChain Python overview：<https://docs.langchain.com/oss/python/langchain/overview>
- LangChain quickstart：<https://docs.langchain.com/oss/python/langchain/quickstart>

官方文档确认的 v1 关键变化：

- `create_agent` 是 LangChain v1 创建 agent 的标准入口，导入路径是 `from langchain.agents import create_agent`。
- v1 的 `langchain` 命名空间更聚焦，主要保留 agents、messages、tools、chat model 初始化、embeddings 等 agent 相关核心能力。
- 旧版 chains、retrievers、hub、部分 community 导出等功能迁移到 `langchain-classic`。
- LangChain 的 agent 构建在 LangGraph 之上，但入门阶段不需要先学习 LangGraph 才能使用 `create_agent`。

## 核心概念讲解

LangChain v1 可以先理解成一个更收敛的 agent 框架：

```text
Agent = Model + Tools + Prompt + Middleware + Loop
```

其中：

- `Model`：真正调用大模型的部分，例如 OpenAI、Anthropic、Google、Ollama 等 provider。
- `Tools`：模型可以请求调用的 Python 函数或工具。
- `Prompt`：告诉 agent 角色、边界和行为偏好的系统提示词。
- `Middleware`：在模型调用、工具调用、上下文处理等环节插入控制逻辑。
- `Loop`：agent 的运行循环，通常是“模型思考 -> 需要工具就调用工具 -> 再把工具结果交给模型 -> 直到给出最终回答”。

学习 v1 时，优先看 `langchain.agents.create_agent` 这一条主线。遇到旧教程里的 `LLMChain`、`ConversationChain`、`langchain.chains`、`langchain.retrievers` 或 `langchain.hub`，不要立刻照抄；先查当前官方文档，看它是否已经迁移到 `langchain-classic` 或被新的 agent / LangGraph 写法替代。

## Java 开发者视角类比

可以把这次版本边界理解成一次框架模块拆分：

- `langchain` 类似新的精简主模块，只暴露当前主推的核心 API。
- `langchain-classic` 类似 legacy 兼容模块，保留旧功能，方便迁移旧项目。
- `create_agent` 类似一个高层工厂方法，帮你组装 model、tools、prompt 和执行循环。
- `LangGraph` 更像底层编排引擎，适合需要精细控制状态、节点和流程时再深入。

这和 Java 生态里 Spring 把旧模块迁走、主包只保留推荐能力的思路有点像：旧 API 不一定马上消失，但新项目应该优先使用官方当前推荐的入口。

## 代码实践

本节的实践目标是确认“导入路径该看哪里”。按官方 v1 文档，最小导入应长这样：

```python
from langchain.agents import create_agent
```

当前本地环境尚未同步依赖，使用 `.venv\Scripts\python.exe` 验证时出现：

```text
ModuleNotFoundError: No module named 'langchain'
```

这说明仓库结构和计划已经准备好，但虚拟环境里还没有安装 `pyproject.toml` 中声明的依赖。进入 LC-02 前，需要先恢复 `uv` 命令或用其他方式同步依赖。

## 对比示例

看到下面几种导入方式时，可以这样判断它们和 v1 主线的关系：

```python
from langchain.agents import create_agent
```

```python
from langchain.chains import LLMChain
```

```python
from langchain.tools import tool
```

- 第 1 个是 v1 agent 主入口。
- 第 2 个是旧教程中常见写法，遇到时优先查是否应改用 v1 agent 或 `langchain-classic`。
- 第 3 个仍属于 v1 精简命名空间中的工具相关能力。

## 常见坑

- 看到中文博客或旧视频里的 `chain` 示例就直接复制，容易撞上 v1 包路径变化。
- 把 LangChain、LangGraph、LangSmith 混成一个东西。它们有关联，但职责不同：LangChain 写 agent，LangGraph 做底层编排，LangSmith 做 tracing、debug 和 evaluation。
- 安装了 `langchain` 不等于安装了具体模型 provider 的集成包。比如 OpenAI、Anthropic、Google、Ollama 等通常还需要对应 provider 包或 extra。
- 本地 `.venv` 存在不代表依赖已安装，需要用 `uv sync` 或等价命令同步。

## 本次总结

LC-01 的核心收获：以后学习 LangChain，先确认资料是否面向 v1。当前主线从 `create_agent` 开始，旧的 chains/retrievers/hub 相关资料要谨慎处理，必要时查 `langchain-classic` 或官方迁移说明。

下一节 LC-02 会进入最小 agent：创建一个能回答问题并调用工具的 agent。在动手前，需要先处理本地依赖同步问题。

## 建议 Git commit message

```text
LC-01：完成 LangChain v1 版本边界笔记
```
