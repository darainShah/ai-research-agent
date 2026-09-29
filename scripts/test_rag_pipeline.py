from app.rag_pipeline import RAGPipeline


DOCUMENT_ID = "78c109fd130398f79b4fb33ff925c4ff7cda2fab8c3b51f2cb83dd970a52627f"


pipeline = RAGPipeline()

question = "What is AQI and how is it calculated?"

result = pipeline.answer(
    question=question,
    document_id=DOCUMENT_ID
)

print("\n==============================")
print("RAG PIPELINE TEST")
print("==============================")

print("\nQUESTION:")
print(result["question"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(
        f"Page={source['page']} "
        f"Vector Score={source['vector_score']:.4f}"
    )

print("\nCITATION VALIDATION:")
print(result["citation_validation"])

pipeline.close()