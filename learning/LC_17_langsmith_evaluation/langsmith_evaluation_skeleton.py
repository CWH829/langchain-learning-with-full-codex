"""LC-17：LangSmith Evaluation 手写骨架。

目标：
1. 创建一个包含 3 条样例的离线评测 dataset。
2. 把 LC-13 的 2-step RAG 包装成 target function。
3. 编写答案关键词与检索来源两个 evaluator。
4. 使用 Client.evaluate(...) 运行 experiment。

说明：
- 请先由学习者手动在本地 .env 中配置 LANGSMITH_API_KEY。
- 不要在代码中硬编码或打印 API Key。
- dataset 通常只需创建一次；重复练习时请复用或修改名称。
- 本文件保留关键 TODO，建议学习者亲手补全。
"""

from __future__ import annotations

import os
from typing import Any
from uuid import UUID

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import InMemoryVectorStore
from langsmith import Client

from learning.LC_13_two_step_rag.two_step_rag_skeleton import (
    answer_question,
    build_chat_model,
    build_vector_store,
)

# dataset
DATASET_NAME = "lc17-rag-mini-eval"

# examples
EVALUATION_EXAMPLES = [
    {
        "inputs": {
            "question": "What isolates one short-term memory conversation from another?"
        },
        "outputs": {
            "required_keywords": ["thread_id"],
            "expected_sources": ["lc-10"],
        },
    },
    {
        "inputs": {
            "question": "What two fields organize long-term memory records?"
        },
        "outputs": {
            "required_keywords": ["namespace", "key"],
            "expected_sources": ["lc-11"],
        },
    },
    {
        "inputs": {
            "question": "How many chat model calls does two-step RAG normally need per question?"
        },
        "outputs": {
            "required_keywords": ["one"],
            "expected_sources": ["lc-13"],
        },
    },
]


def build_client() -> Client:
    """加载环境变量并创建 LangSmith Client。"""
    # 1：调用 load_dotenv()。
    # 2：检查 LANGSMITH_API_KEY 是否存在，但不要打印它。
    # 3：返回 Client()。
    load_dotenv()
    if os.getenv("LANGSMITH_API_KEY"):
        return Client()
    raise Exception("请先配置 LANGSMITH_API_KEY。")


# 这里是直接就会创建在 LangSmith 中了。
def create_dataset_once(client: Client) -> UUID:
    """首次练习时创建 dataset 和 examples，并返回 dataset ID。"""
    # 1：调用 client.create_dataset(...)。
    # - dataset_name 使用 DATASET_NAME。
    # - description 说明它是 LC-17 的 2-step RAG mini eval。
    dataset = client.create_dataset(dataset_name=DATASET_NAME, description="LC-17 two-step RAG mini eval")

    # 2：调用 langsmith client.create_examples(...) 批量上传样例。
    # - dataset_id 使用刚创建 dataset 的 id。
    # - examples 使用 EVALUATION_EXAMPLES。
    client.create_examples(dataset_id=dataset.id, examples=EVALUATION_EXAMPLES)

    # 3：返回 dataset.id。
    # 提醒：这个函数通常只执行一次。若同名 dataset 已存在，请在 LangSmith UI
    # 中复用它，或临时修改 DATASET_NAME 后再创建。
    return dataset.id


# model 和 vector_store 在 experiment 开始前构造一次，避免每条样例重复初始化。——单例
MODEL: BaseChatModel | None = None
VECTOR_STORE: InMemoryVectorStore | None = None


def prepare_target_dependencies() -> None:
    """准备 target function 需要复用的依赖。"""
    global MODEL, VECTOR_STORE

    # 1：调用 build_chat_model()。
    # 2：调用 build_vector_store()。
    # 3：分别赋值给 MODEL 和 VECTOR_STORE。
    if not MODEL:
        MODEL = build_chat_model()
    if not VECTOR_STORE:
        VECTOR_STORE = build_vector_store()


def rag_target(inputs: dict[str, Any]) -> dict[str, Any]:
    """把 LC-13 的 2-step RAG 包装成 LangSmith target function。"""
    # 1：读取 inputs["question"]。
    # 2：确认 MODEL 和 VECTOR_STORE 已准备好。
    # 3：调用 answer_question(MODEL, VECTOR_STORE, question, k=2)。
    # 4：从 documents 的 metadata 中提取 source。
    # 5：返回：
    # {
    #     "answer": answer,
    #     "sources": sources,
    # }
    question = inputs["question"]
    if MODEL is not None and VECTOR_STORE is not None:
        answer, documents = answer_question(MODEL, VECTOR_STORE, question, k=2)
        sources = [doc.metadata["source"] for doc in documents]
        return {
            "answer": answer,
            "sources": sources,  # lc-xx
        }
    raise Exception("MODEL 和 VECTOR_STORE 未准备好！")


# evaluator 1
def answer_contains_required_keywords(
        outputs: dict[str, Any],
        reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    """检查回答是否包含 reference outputs 中的全部必要关键词。"""
    # 1：读取 outputs["answer"] 并统一转为小写。
    # 2：读取 reference_outputs["required_keywords"]。
    # 3：使用 all(...) 判断每个关键词是否都出现在回答中。
    #
    # Python 提示：
    # all(condition for item in items) 会在所有 condition 为 True 时返回 True。
    answer = outputs["answer"].lower()
    required_keywords = reference_outputs["required_keywords"]
    return {
        "key": "answer_contains_required_keywords",
        "score": all(keyword in answer for keyword in required_keywords), # true / false
    }


# evaluator 2
def retrieved_expected_source(
        outputs: dict[str, Any],
        reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    """检查实际检索来源是否覆盖 reference outputs 中的期望来源。"""
    # 1：读取 outputs["sources"]。
    # 2：读取 reference_outputs["expected_sources"]。
    # 3：判断每个期望来源是否都包含在实际来源中。
    sources = outputs["sources"]  # lc-xx
    expected_sources = reference_outputs["expected_sources"]  # lc-xx
    return {
        "key": "retrieved_expected_source",
        "score": all(source in sources for source in expected_sources), # true / false
    }


# 包含执行 target function，以及对其 evaluator 2次的整个 experiment。
def run_experiment(client: Client) -> None:
    """在已有 dataset 上运行一次离线评测 experiment。"""
    # 1：调用 prepare_target_dependencies()。
    # 2：调用 client.evaluate(...)。

    prepare_target_dependencies()

    # langsmith evalution：
    experiment_result = client.evaluate(
        rag_target,  # target function
        data=DATASET_NAME,  # dataset 和 examples 在 evaluate 前已经配置好
        evaluators=[
            answer_contains_required_keywords,
            retrieved_expected_source,
        ],  # 2个 evaluator
        experiment_prefix="lc17-rag-mini-eval",  # 实验名
        description="Evaluate LC-13 two-step RAG with deterministic evaluators.",  # 确定性评估
        metadata={"stage": "LC-17", "system": "two-step-rag"},
    )

    # 3：打印 experiment 结果对象，观察其中给出的 LangSmith URL。
    print(f"experiment result: {experiment_result}")
    return None


def main() -> None:
    """选择创建数据集或运行 experiment。"""
    client = build_client()

    # 首次练习：取消下一行注释，创建 dataset；成功后再次注释。（因为 langsmith 中已经创建了 dataset）
    # dataset_id = create_dataset_once(client)
    # print(f"created dataset in LangSmith: {dataset_id}")

    # dataset 已存在后，取消下一行注释运行 experiment。
    run_experiment(client)

    print(
        "请按骨架注释选择：首次创建 dataset，或在已有 dataset 上运行 experiment。"
    )


if __name__ == "__main__":
    main()
