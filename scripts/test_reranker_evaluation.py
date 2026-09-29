from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


EVALUATION_CASES = [
    {
        "question": "What is attention?",
        "relevant_pages": [1],
    },
    {
        "question": "What are Q, K, and V?",
        "relevant_pages": [1,2,3,5],
    },
    {
        "question": "What is self-attention?",
        "relevant_pages": [4],
    },
]


retriever = Retriever()
reranker = Reranker()


print("\n==============================")
print("RERANKER EVALUATION")
print("==============================")


for case in EVALUATION_CASES:

    question = case["question"]
    relevant_pages = case["relevant_pages"]

    results = retriever.retrieve(
        query=question,
        top_k=10
    )

    reranked_results = reranker.rerank(
        query=question,
        results=results,
        top_k=3
    )

    retrieved_pages = [
        item["result"].payload["metadata"]["page"]
        for item in reranked_results
    ]

    hit = any(
        page in relevant_pages
        for page in retrieved_pages
    )

    print("\n------------------------------")
    print(f"Question: {question}")
    print(f"Expected pages: {relevant_pages}")
    print(f"Retrieved pages: {retrieved_pages}")
    print(f"Top-3 Hit: {'PASS' if hit else 'FAIL'}")


retriever.close()

print("\n==============================")
print("EVALUATION COMPLETE")
print("==============================")
