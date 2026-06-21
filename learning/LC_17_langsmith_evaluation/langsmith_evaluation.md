# LC-17：LangSmith Evaluation

## 1. 本阶段目标

完成本阶段后，应能够：

1. 解释 dataset、example、target function、evaluator 和 experiment 的关系。
2. 使用 `langsmith.Client` 创建一个小型离线评测数据集。
3. 把 LC-13 的 2-step RAG 包装成符合评测要求的 target function。
4. 编写至少两个确定性 evaluator，分别检查回答内容与检索来源。
5. 使用 `client.evaluate(...)` 运行 experiment，并在 LangSmith UI 中比较每条样例的结果。
6. 理解离线评测适合回归测试，但少量样例与关键词判断不能代表完整质量。

本阶段先完成 deterministic evaluation（确定性评测）。LLM-as-judge、pairwise comparison（两两比较）、
在线评测和复杂统计分析只作为后续扩展，不放进第一轮手写实践。

## 2. 官方文档核对

本阶段以 LangSmith 官方文档为准：

- Evaluation 总览：
  <https://docs.langchain.com/langsmith/evaluation>
- Evaluation quickstart：
  <https://docs.langchain.com/langsmith/evaluation-quickstart>
- Evaluate an application：
  <https://docs.langchain.com/langsmith/evaluate-llm-application>
- Manage datasets：
  <https://docs.langchain.com/langsmith/manage-datasets>

截至 2026-06-21，官方文档确认：

1. 离线评测的核心组成是 dataset、target function 和 evaluators。
2. dataset 由 examples 组成；每条 example 通常包含 `inputs` 和可选的
   `outputs`（reference outputs，参考输出）。
3. target function 接收一条 example 的 inputs，并返回字典形式的 outputs。
4. evaluator 可以读取 `inputs`、target 的 `outputs` 和 `reference_outputs`，
   返回布尔值、分数或带 key/score 的结果。
5. `Client.evaluate(...)` 会对数据集逐条运行 target 和 evaluators，并把结果记录为 experiment。
6. `experiment_prefix`、`description` 和 `metadata` 可用于识别与比较不同实验。

## 3. 核心概念

### 3.1 Dataset 与 Example

dataset 是一组固定的**测试案例**。example 是其中一条案例：

```python
{
    "inputs": {
        "question": "What isolates short-term memory conversations?"
    },
    "outputs": {
        "required_keywords": ["thread_id"],
        "expected_sources": ["lc-10"],
    },
}
```

这里的 `outputs` 不是模型实际回答，而是评测时使用的 reference outputs。

### 3.2 Target Function

target function 是“被测系统”的统一入口：

```python
def rag_target(inputs: dict) -> dict:
    question = inputs["question"]
    answer, documents = answer_question(...)
    return {
        "answer": answer,
        "sources": [document.metadata["source"] for document in documents],
    }
```

它只关心一条输入如何变成一条实际输出。LangSmith 负责遍历数据集、记录运行结果并调用 evaluators。

### 3.3 Evaluator

evaluator 用明确规则判断一条输出是否满足某个维度。

本阶段使用两个 evaluator：

- `answer_contains_required_keywords`：回答是否包含所有**必要关键词**。
- `retrieved_expected_source`：实际检索来源是否包含**期望来源**。

两个维度应分开记录。否则，只得到一个总分时，很难判断失败来自 retrieval 还是 generation。

### 3.4 Experiment

experiment（实验） 是“某个 target 版本在某个 dataset 上的一次完整运行”。

```mermaid
flowchart LR
    A["Dataset：3 条 examples"] --> B["Target：LC-13 2-step RAG"]
    B --> C["Actual outputs"]
    C --> D["答案关键词 evaluator"]
    C --> E["来源命中 evaluator"]
    D --> F["Experiment results"]
    E --> F
```

同一数据集可以反复运行不同 prompt、model、retrieval `k` 或代码版本，然后比较实验结果。

## 4. 为什么复用 LC-13

LC-13 已经提供：

- 固定知识文档。
- 可重复构造的 vector store。
- `retrieve -> format -> generate` 流程。
- 同时返回 answer 和真实 documents 的 `answer_question(...)`。

这让 LC-17 能把注意力放在“如何评测”，而不是重新实现 RAG。尤其是保留真实 documents，
可以单独评价 retrieval，不必让模型自己声称使用了哪些来源。

## 5. 手写实践任务

骨架文件：

- `langsmith_evaluation_skeleton.py`
- `langsmith_evaluation_skeleton.origin.py`

建议按以下顺序补全：

1. 手动确认 `.env` 中已有 `LANGSMITH_API_KEY`。
2. 创建 `Client` 并上传 3 条 evaluation examples。
3. 构造一次可复用的 model 和 vector store。
4. 完成 `rag_target(inputs)`，返回 `answer` 和 `sources`。
5. 完成答案关键词 evaluator。
6. 完成检索来源 evaluator。
7. 调用 `client.evaluate(...)` 运行 experiment。
8. 在 LangSmith UI 中观察逐条结果、错误、耗时和 evaluator 分数。

> 数据集创建只需执行一次。重复运行前，可在 UI 中复用已有 dataset，或临时修改
> `DATASET_NAME`，避免重复创建同名数据集造成困惑。

## 6. 重点观察

运行后重点回答：

1. target function 收到的是整条 example，还是仅 `inputs`？
2. target 返回的 `sources` 来自真实 documents，还是模型生成文本？
3. 某条样例失败时，是关键词 evaluator 失败，还是来源 evaluator 失败？
4. 未知问题是否检索到了低相关文档？这会怎样影响来源命中指标？
5. 相同 dataset 更换 model、prompt 或 `k` 后，experiment 是否方便比较？
6. evaluator 本身是否可能误判？

## 7. 评测边界

### 7.1 关键词命中不等于语义正确

回答包含 `thread_id`，不代表它正确解释了 thread isolation。关键词 evaluator 的优点是便宜、
稳定、易排错；缺点是不能理解完整语义。

### 7.2 来源命中不等于回答 grounded

检索到了正确文档，不代表最终回答忠实使用了该文档。retrieval 和 generation 应拆成不同指标。

### 7.3 三条数据只是教学闭环

最小数据集用于熟悉 API，不足以代表真实质量。后续项目中应逐步加入：

- 正常问题、边界问题和未知问题。
- 不同表达方式与语言。
- 容易混淆的相邻概念。
- 生产 traces 中发现的真实失败案例。

### 7.4 数据与密钥安全

不要把 API Key 写进 dataset、metadata、inputs 或 outputs。上传真实业务样例前，还要检查隐私信息、
内部文档和用户数据是否允许进入 LangSmith。

## 8. 阶段完成标准

满足以下条件后，可完成 LC-17：

1. LangSmith 中存在一个包含 3 条样例的 dataset。
2. target function 能返回结构稳定的 `answer` 和 `sources`。
3. 至少两个 evaluator 能分别输出评测结果。
4. 成功产生一个 experiment，并能解释逐条结果。
5. 能指出确定性 evaluator 的至少两个局限。

