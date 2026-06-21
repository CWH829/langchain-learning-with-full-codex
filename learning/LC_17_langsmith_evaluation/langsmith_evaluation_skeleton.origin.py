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

from dotenv import load_dotenv
from langsmith import Client

from learning.LC_13_two_step_rag.two_step_rag_skeleton import (
    answer_question,
    build_chat_model,
    build_vector_store,
)

DATASET_NAME = "lc17-rag-mini-eval"

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
    # TODO 1：调用 load_dotenv()。
    # TODO 2：检查 LANGSMITH_API_KEY 是否存在，但不要打印它。
    # TODO 3：返回 Client()。
    raise NotImplementedError


def create_dataset_once(client: Client) -> str:
    """首次练习时创建 dataset 和 examples，并返回 dataset ID。"""
    # TODO 1：调用 client.create_dataset(...)。
    # - dataset_name 使用 DATASET_NAME。
    # - description 说明它是 LC-17 的 2-step RAG mini eval。
    #
    # TODO 2：调用 client.create_examples(...) 批量上传样例。
    # - dataset_id 使用刚创建 dataset 的 id。
    # - examples 使用 EVALUATION_EXAMPLES。
    #
    # TODO 3：返回 dataset.id。
    #
    # 提醒：这个函数通常只执行一次。若同名 dataset 已存在，请在 LangSmith UI
    # 中复用它，或临时修改 DATASET_NAME 后再创建。
    raise NotImplementedError


# model 和 vector_store 在 experiment 开始前构造一次，避免每条样例重复初始化。
MODEL = None
VECTOR_STORE = None


def prepare_target_dependencies() -> None:
    """准备 target function 需要复用的依赖。"""
    global MODEL, VECTOR_STORE

    # TODO 1：调用 build_chat_model()。
    # TODO 2：调用 build_vector_store()。
    # TODO 3：分别赋值给 MODEL 和 VECTOR_STORE。
    raise NotImplementedError


def rag_target(inputs: dict[str, Any]) -> dict[str, Any]:
    """把 LC-13 的 2-step RAG 包装成 LangSmith target function。"""
    # TODO 1：读取 inputs["question"]。
    # TODO 2：确认 MODEL 和 VECTOR_STORE 已准备好。
    # TODO 3：调用 answer_question(MODEL, VECTOR_STORE, question, k=2)。
    # TODO 4：从 documents 的 metadata 中提取 source。
    # TODO 5：返回：
    # {
    #     "answer": answer,
    #     "sources": sources,
    # }
    raise NotImplementedError


def answer_contains_required_keywords(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> bool:
    """检查回答是否包含 reference outputs 中的全部必要关键词。"""
    # TODO 1：读取 outputs["answer"] 并统一转为小写。
    # TODO 2：读取 reference_outputs["required_keywords"]。
    # TODO 3：使用 all(...) 判断每个关键词是否都出现在回答中。
    #
    # Python 提示：
    # all(condition for item in items) 会在所有 condition 为 True 时返回 True。
    raise NotImplementedError


def retrieved_expected_source(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> bool:
    """检查实际检索来源是否覆盖 reference outputs 中的期望来源。"""
    # TODO 1：读取 outputs["sources"]。
    # TODO 2：读取 reference_outputs["expected_sources"]。
    # TODO 3：判断每个期望来源是否都包含在实际来源中。
    raise NotImplementedError


def run_experiment(client: Client) -> None:
    """在已有 dataset 上运行一次离线评测 experiment。"""
    # TODO 1：调用 prepare_target_dependencies()。
    # TODO 2：调用 client.evaluate(...)。
    #
    # 建议参数：
    # - target=rag_target
    # - data=DATASET_NAME
    # - evaluators=[
    #       answer_contains_required_keywords,
    #       retrieved_expected_source,
    #   ]
    # - experiment_prefix="lc17-rag-mini-eval"
    # - description="Evaluate LC-13 two-step RAG with deterministic evaluators."
    # - metadata={"stage": "LC-17", "system": "two-step-rag"}
    #
    # TODO 3：打印 experiment 结果对象，观察其中给出的 LangSmith URL。
    raise NotImplementedError


def main() -> None:
    """选择创建数据集或运行 experiment。"""
    client = build_client()

    # 首次练习：取消下一行注释，创建 dataset；成功后再次注释。
    # dataset_id = create_dataset_once(client)
    # print(f"created dataset: {dataset_id}")

    # dataset 已存在后，取消下一行注释运行 experiment。
    # run_experiment(client)

    print(
        "请按骨架注释选择：首次创建 dataset，或在已有 dataset 上运行 experiment。"
    )


if __name__ == "__main__":
    main()
