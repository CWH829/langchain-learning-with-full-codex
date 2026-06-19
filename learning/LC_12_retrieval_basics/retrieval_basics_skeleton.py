"""LC-12：Retrieval 基础手写骨架。

目标：
1. 使用 Document 表示知识资料。
2. 使用 RecursiveCharacterTextSplitter 切分文档。
3. 使用 Embeddings + InMemoryVectorStore 建立最小向量索引。
4. 通过 similarity_search 或 retriever.invoke 做 top-k 检索。

说明：
- 本文件保留关键 TODO，建议学习者亲手补全。
- KeywordEmbeddings 是离线学习用的极小 embedding，不是生产方案。
"""

from __future__ import annotations

import math
from collections import Counter

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


class KeywordEmbeddings(Embeddings):
    """用于本地学习的极小关键词 embedding。

    它只统计固定词表中的词频，目的是让 vector store 流程可以离线跑通。
    真实项目应替换为 OpenAI、DashScope、Voyage、本地模型等 embedding。
    """

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
        "split",
        "embedding",
        "vector",
        "rag",
    ]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """把一组文档文本转成向量。"""
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """把单条查询文本转成向量。"""
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        words = Counter(text.lower().replace("-", " ").split()) # - 以及 空格，分隔
        vector = [float(words.get(word, 0)) for word in self.vocabulary] # text对应词汇表中的词频 作为向量
        length = math.sqrt(sum(value * value for value in vector)) # 向量长度。Σ sigma 求和。
        if length == 0:
            return vector
        return [value / length for value in vector]


RAW_NOTES = [
    {
        "source": "lc-10",
        "topic": "short-term-memory",
        "text": (
            "Short-term memory is thread-scoped memory. LangChain agents can use a "
            "checkpointer with configurable thread_id to keep messages inside one "
            "conversation thread. Different thread ids are isolated."
        ),
    },
    {
        "source": "lc-11",
        "topic": "long-term-memory",
        "text": (
            "Long-term memory stores user preferences across threads. A store uses "
            "namespace and key to save structured data such as language, tone, topic, "
            "and other user profile fields."
        ),
    },
    {
        "source": "lc-07",
        "topic": "runtime-context",
        "text": (
            "Runtime context passes call-specific data into an agent run. Tools can "
            "receive ToolRuntime and read runtime.context, runtime.state, and runtime.store."
        ),
    },
    {
        "source": "lc-12",
        "topic": "retrieval",
        "text": (
            "Retrieval turns documents into searchable chunks. Text splitters create "
            "document chunks, embeddings turn text into vectors, and vector stores "
            "return the most relevant documents for a query."
        ),
    },
]


def build_source_documents() -> list[Document]:
    """把原始资料转换为 Document 列表。"""
    # 1. 遍历 RAW_NOTES。
    # 2. 为每条资料创建 Document。
    # 3. page_content 使用 note["text"]。
    # 4. metadata 至少保留 source 和 topic。
    # 5. 可选：给 Document 设置稳定 id，例如 f"{note['source']}-{note['topic']}"。
    print(Document.model_fields) # 看看 Document 有哪些固定参数
    return [
        Document(
            page_content=note["text"],
            metadata={"source": note["source"], "topic": note["topic"]},
            id=f"{note['source']}-{note['topic']}",
        )
        for note in RAW_NOTES
    ]


def split_documents(documents: list[Document]) -> list[Document]:
    """切分 Document，保留 metadata。"""
    # 1. 创建 RecursiveCharacterTextSplitter。
    # 2. chunk_size 可先设为 180。
    # 3. chunk_overlap 可先设为 30。
    # 4. 设置 add_start_index=True，观察 chunk metadata 中的 start_index。
    # 5. 调用 splitter.split_documents(documents)。
    #
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=180,
        chunk_overlap=30,
        add_start_index=True,
    )
    return splitter.split_documents(documents) # 返回切分后的 Document 列表


def build_vector_store(chunks: list[Document]) -> InMemoryVectorStore:
    """把 chunk 写入内存向量库。"""
    embeddings = KeywordEmbeddings()

    # 1. 使用 InMemoryVectorStore.from_documents(...)。
    # 2. documents 传入 chunks。
    # 3. embedding 传入 embeddings。
    #
    return InMemoryVectorStore.from_documents( # 文本转向量，存入 vector store 向量数据库
        documents=chunks, # 切分后的 Document
        embedding=embeddings, # 自定义 embedding
    )


# 检索方式 1：直接用 vector store，similarity_search
def retrieve_with_similarity_search(
    vector_store: InMemoryVectorStore, # vector store 向量数据库
    query: str,
    k: int = 3,
) -> list[Document]:
    """使用 vector store 直接做相似度检索。"""
    # 1. 调用 vector_store.similarity_search(query, k=k)。
    # 2. 返回检索到的 Document 列表。
    return vector_store.similarity_search(query, k=k)


# 检索方式 2：转成 retriever，invoke
def retrieve_with_retriever(
    vector_store: InMemoryVectorStore,
    query: str,
    k: int = 3,
) -> list[Document]:
    """先转成 retriever，再调用 invoke。"""
    # 1. 调用 vector_store.as_retriever(search_kwargs={"k": k})。
    # 2. 调用 retriever.invoke(query)。
    # 3. 返回检索到的 Document 列表。
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)


def print_documents(title: str, documents: list[Document]) -> None:
    """打印检索结果，重点观察 metadata 和 page_content。"""
    print(f"\n=== {title} ===") # 检索方式
    for index, document in enumerate(documents, start=1):
        print(f"\n--- result {index} ---")
        print("metadata:", document.metadata)
        print("content:", document.page_content)
        print("content size:", len(document.page_content))


def run_retrieval_demo() -> None:
    """串联 LC-12 的核心实践流程。"""
    source_documents = build_source_documents() # 原始 Doc
    chunks = split_documents(source_documents) # 切分后的 Doc
    vector_store = build_vector_store(chunks) # 嵌入向量库

    print(f"原始 doc count: {len(source_documents)}")
    print(f"切分后的 count: {len(chunks)}")

    queries = [
        "How does thread memory work?",
        "Where are user preferences stored?",
        "Why does retrieval split documents into vectors?",
        "Where do tools use runtime context?",
    ]

    for query in queries:
        search_results = retrieve_with_similarity_search(vector_store, query, k=2)
        print_documents(f"similarity_search: {query}", search_results)

        retriever_results = retrieve_with_retriever(vector_store, query, k=2)
        print_documents(f"retriever.invoke: {query}", retriever_results)


def main() -> None:
    """最小手动验证入口。"""
    run_retrieval_demo()

if __name__ == "__main__":
    main()
