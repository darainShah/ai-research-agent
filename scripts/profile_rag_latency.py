import time

from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore
from app.retrieval.reranker import Reranker
from app.generation.llm import LLM
from app.retrieval.context_builder import build_context


DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)

QUESTION = "What is the formula for self-attention?"


def timed(label, function):
    start = time.perf_counter()

    result = function()

    elapsed = time.perf_counter() - start

    print(f"{label:<30} {elapsed:.3f} seconds")

    return result, elapsed


def main():

    print("\n==============================")
    print("RAG LATENCY PROFILING")
    print("==============================")

    embedder = Embedder()
    vector_store = VectorStore()
    reranker = Reranker()
    llm = LLM()

    try:

        print("\n------------------------------")
        print("MODEL / PIPELINE INITIALIZATION")
        print("------------------------------")

        print("Models initialized successfully.")

        print("\n------------------------------")
        print("PIPELINE STAGES")
        print("------------------------------")

        _, rewrite_time = timed(
            "Question rewriting",
            lambda: llm.rewrite_question(
                question=QUESTION,
                chat_history=[]
            )
        )

        query_vector, embedding_time = timed(
            "Query embedding",
            lambda: embedder.embed_text(QUESTION)
        )

        results, retrieval_time = timed(
            "Vector retrieval",
            lambda: vector_store.search(
                query_vector=query_vector,
                limit=10,
                document_id=DOCUMENT_ID
            )
        )

        results = [
            result
            for result in results
            if result.score >= 0.30
        ]

        reranked, reranker_time = timed(
            "Cross-encoder reranking",
            lambda: reranker.rerank(
                query=QUESTION,
                results=results,
                top_k=3
            )
        )

        final_results = [
            item["result"]
            for item in reranked
        ]

        context = build_context(final_results)

        _, generation_time = timed(
            "LLM answer generation",
            lambda: llm.generate(
                question=QUESTION,
                context=context,
                chat_history=[]
            )
        )

        total_time = (
            rewrite_time
            + embedding_time
            + retrieval_time
            + reranker_time
            + generation_time
        )

        print("\n------------------------------")
        print("LATENCY BREAKDOWN")
        print("------------------------------")

        print(
            f"Total measured pipeline time: "
            f"{total_time:.3f} seconds"
        )

        print("\n==============================")
        print("PROFILING COMPLETE")
        print("==============================")

    finally:

        vector_store.close()


if __name__ == "__main__":
    main()
