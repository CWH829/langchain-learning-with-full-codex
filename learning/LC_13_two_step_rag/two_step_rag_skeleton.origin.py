"""LC-13：2-step RAG 手写骨架。

目标：
1. 复用 LC-12 的 Document、Embeddings 和 InMemoryVectorStore。
2. 手写 retrieve -> format -> generate 固定 pipeline。
3. 每个问题只进行一次 chat model 调用。
4. 同时返回答案与真实检索来源。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- KeywordEmbeddings 只用于离线教学，不是生产方案。
- 查询先使用英文，因为固定词表不能理解中文语义。
"""

from __future__ import annotations

import math
import os
from collections import Counter

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.vectorstores import InMemoryVectorStore


class KeywordEmbeddings(Embeddings):
    """用于本地学习的极小关键词 embedding。"""

    vocabulary = [
        "agent",
        "tool",
        "runtime",
        "context",
        "memory",
        "thread",
        "store",
        "user",
        "preference",
        "retrieval",
        "document",
        "embedding",
        "vector",
        "rag",
        "generate",
        "answer",
    ]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        words = Counter(text.lower().replace("-", " ").split())
        vector = [float(words.get(word, 0)) for word in self.vocabulary]
        length = math.sqrt(sum(value * value for value in vector))
        if length == 0:
            return vector
        return [value / length for value in vector]


KNOWLEDGE_DOCUMENTS = [
    Document(
        page_content=(
            "Short-term memory is thread-scoped. A checkpointer stores conversation "
            "state, and configurable thread_id isolates one conversation from another."
        ),
        metadata={"source": "lc-10", "topic": "short-term-memory"},
    ),
    Document(
        page_content=(
            "Long-term memory stores user preferences across conversation threads. "
            "A store uses namespace and key, while user_id commonly selects the namespace."
        ),
        metadata={"source": "lc-11", "topic": "long-term-memory"},
    ),
    Document(
        page_content=(
            "Retrieval converts documents into searchable representations. At query time, "
            "a retriever returns relevant documents before a RAG system generates an answer."
        ),
        metadata={"source": "lc-12", "topic": "retrieval"},
    ),
    Document(
        page_content=(
            "Two-step RAG always retrieves context before generation. It uses a predictable "
            "pipeline and normally needs one chat model call for each user question."
        ),
        metadata={"source": "lc-13", "topic": "two-step-rag"},
    ),
]


def build_vector_store() -> InMemoryVectorStore:
    """构建本阶段使用的内存知识库。"""
    return InMemoryVectorStore.from_documents(
        documents=KNOWLEDGE_DOCUMENTS,
        embedding=KeywordEmbeddings(),
    )


def build_chat_model():
    """复用仓库现有的 DeepSeek OpenAI-compatible 环境变量约定。"""
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("缺少环境变量 DEEPSEEK_API_KEY")

    return init_chat_model(
        model=os.getenv("MODEL_NAME", "deepseek-v4-flash"),
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        api_key=api_key,
        base_url=os.getenv("MODEL_BASE_URL", "https://api.deepseek.com"),
        temperature=0,
        timeout=30,
        max_retries=5,
    )


def retrieve_documents(
    vector_store: InMemoryVectorStore,
    question: str,
    k: int = 2,
) -> list[Document]:
    """步骤 1：根据原始问题检索文档。"""
    # TODO 1：
    # 1. 调用 vector_store.similarity_search(...)。
    # 2. query 使用原始 question。
    # 3. 把 k 传给检索方法。
    # 4. 返回 list[Document]。
    #
    # 参考形状：
    # return vector_store.similarity_search(...)
    raise NotImplementedError


def format_context(documents: list[Document]) -> str:
    """把检索文档转换为适合放入 prompt 的上下文。"""
    # TODO 2：
    # 1. 遍历 documents，可使用 enumerate(..., start=1)。
    # 2. 每段保留 source、topic 和 page_content。
    # 3. 使用清晰分隔符连接不同文档。
    # 4. 返回单个 str。
    #
    # 推荐格式：
    # [Document 1]
    # source: ...
    # topic: ...
    # content: ...
    raise NotImplementedError


def build_rag_messages(question: str, context: str) -> list[SystemMessage | HumanMessage]:
    """为一次 2-step RAG 生成调用构造 messages。"""
    # TODO 3：
    # 1. 创建 SystemMessage。
    # 2. 要求模型只根据检索上下文回答；资料不足时明确说不知道。
    # 3. 要求把 <context> 中的内容视为数据，不执行其中的指令。
    # 4. 在 system message 中用 <context>...</context> 包裹 context。
    # 5. 创建 HumanMessage，content 保留原始 question。
    # 6. 返回 [system_message, human_message]。
    #
    # 注意：不要把未知答案偷偷写进 system prompt。
    raise NotImplementedError


def answer_question(
    model,
    vector_store: InMemoryVectorStore,
    question: str,
    k: int = 2,
) -> tuple[str, list[Document]]:
    """串联 retrieve -> format -> generate，并保留真实来源。"""
    # TODO 4：
    # 1. 调用 retrieve_documents(...)。
    # 2. 调用 format_context(...)。
    # 3. 调用 build_rag_messages(...)。
    # 4. 只调用一次 model.invoke(messages)。
    # 5. 确认返回值是 AIMessage。
    # 6. 返回 (response.text, documents)。
    #
    # documents 必须来自真实检索结果，不要让模型编造来源。
    raise NotImplementedError


def print_sources(documents: list[Document]) -> None:
    """打印真实检索来源，便于判断 retrieval 是否正确。"""
    print("\n--- retrieved sources ---")
    for index, document in enumerate(documents, start=1):
        print(
            f"{index}. source={document.metadata.get('source')}, "
            f"topic={document.metadata.get('topic')}"
        )
        print(f"   {document.page_content}")


def run_demo() -> None:
    """运行已知问题与未知问题，对比检索来源和最终答案。"""
    model = build_chat_model()
    vector_store = build_vector_store()

    questions = [
        "How is short-term memory isolated?",
        "What does retrieval do before RAG generates an answer?",
        "What is the capital of France?",
    ]

    for question in questions:
        print(f"\n=== question: {question} ===")

        # TODO 5：
        # 1. 调用 answer_question(...) 并使用 tuple 解包。
        # 2. 先调用 print_sources(sources)。
        # 3. 再打印 answer。
        # 4. 观察未知问题是否仍然检索到无关 top-k 文档。
        #
        # answer, sources = ...
        # print_sources(...)
        # print(...)
        pass


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
