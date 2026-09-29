from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


query = "What is AQI and how is it calculated?"

retriever = Retriever()
reranker = Reranker()

results = retriever.retrieve(
    query=query,
    top_k=10
)

print("\n==============================")
print("DENSE RETRIEVAL")
print("==============================")

for i, result in enumerate(results, start=1):
    print(
        f"{i}. Page={result.payload['metadata']['page']} "
        f"Vector Score={result.score:.4f}"
    )

reranked = reranker.rerank(
    query=query,
    results=results,
    top_k=5
)

print("\n==============================")
print("RERANKED RESULTS")
print("==============================")

for i, item in enumerate(reranked, start=1):

    result = item["result"]

    print(
        f"{i}. Page={result.payload['metadata']['page']} "
        f"Vector Score={result.score:.4f} "
        f"Reranker Score={item['reranker_score']:.4f}"
    )

    print(result.payload["text"][:500])
    print("------------------------------")

retriever.close()