# LC-18 LangGraph Intro Implementation Plan

> **For agentic workers:** 当前会话内联执行。仓库规则优先：不执行 Git commit，不主动运行额外验证，实践代码由学习者手写。

**Goal:** 准备从纯 Python 图递进到 model/tool 循环的 LC-18 学习材料。

**Architecture:** 阶段目录包含完整笔记和一对骨架文件；骨架分为直线图、Router 图和 model/tool 图三个练习区。

**Tech Stack:** Python 3.11+、LangGraph 1.2.5、LangChain 1.3.9、`TypedDict`、LangChain messages/tools。

---

### Task 1：启动阶段

- [x] 将 LC-18 更新为进行中并记录开始时间。

### Task 2：学习笔记

- [x] 核对官方 Graph API。
- [x] 解释核心概念、reducer、消息 state 和 agent 边界。
- [x] 加入生命周期图、Router 图和 model/tool 循环图。
- [x] 整理常见错误与完成标准。

### Task 3：手写骨架

- [x] 创建直线图练习。
- [x] 创建条件分支与汇合练习。
- [x] 创建 model/tool 循环练习。
- [x] 创建 origin 对照副本。

### Task 4：学习执行

- [x] 学习者完成直线图并解释 state 更新。
- [x] 学习者完成 Router 图并观察两条分支。
- [x] 学习者完成 model/tool 图并观察消息链。
- [x] 完成后补充实践记录、阶段摘要和完成时间。
