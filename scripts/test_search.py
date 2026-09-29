from app.retrieval.retriever import Retriever

retriever = Retriever()

query = input("\nEnter your quesition:")

results = retriever.retrieve(
    query=query,
    top_k=5
)

print("\n==============================")
print("RETRIEVAL RESULTS")
print("==============================")

if not results:
    print("No relevant results found.")

for i, result in enumerate(results, start=1):
    metadata = result.payload["metadata"]
    text = result.payload["text"]

    print("\n------------------------------")
    print(f"RESULT: {i}")
    print(f"Source: {metadata['source']}")
    print(f"Page: {metadata['page']}")
    print(f"Score: {result.score:.4f}")
    print("------------------------------")
    print(text)

retriever.close()