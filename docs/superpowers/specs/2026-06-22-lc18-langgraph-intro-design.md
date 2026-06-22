# LC-18 LangGraph 入门学习设计

## 目标

通过“纯 Python 直线图 → Router 条件图 → model/tool 循环”掌握 LangGraph Graph API，并理解它与 LangChain 预构建 agent 的边界。

## 产出

- `learning/LC_18_langgraph_intro/langgraph_intro.md`
- `learning/LC_18_langgraph_intro/langgraph_intro_skeleton.py`
- `learning/LC_18_langgraph_intro/langgraph_intro_skeleton.origin.py`
- `.agents/LANGCHAIN_PLAN.md` 中 LC-18 状态更新

## 边界

- 先看清 state、node、edge、reducer、compile 和 invoke，再引入 LLM。
- LC-18 后半段覆盖 `MessagesState`、`model.bind_tools(...)`、`ToolNode` 和 `tools_condition`。
- persistence、interrupt、streaming、subgraph 和 multi-agent 留待后续。
- 学习者手写实现；骨架只提供函数边界和关键提示。
- 不主动运行环境验证，不执行 Git commit。

## 自检

- 三个递进实践均有对应材料。
- model/tool 内容没有推迟到 LC-19。
- 没有把 multi-agent 等后续主题提前混入。
