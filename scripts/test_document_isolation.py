from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


RESEARCH_DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)

DATABASE_DOCUMENT_ID = (
    "6ddbe50b5f24cc2fd700afb34096125dd85e84624dfd8757381460bfc7ee03c7"
)


def test_document(
    vector_store,
    embedder,
    document_id,
    question,
    expected_filename
):
    query_vector = embedder.embed_text(question)

    results = vector_store.search(
        query_vector=query_vector,
        limit=5,
        document_id=document_id
    )

    print("\n------------------------------")
    print(f"Question: {question}")
    print(f"Expected document: {expected_filename}")
    print(f"Retrieved results: {len(results)}")

    for index, result in enumerate(results, start=1):

        metadata = result.payload["metadata"]

        print(f"\nResult {index}")
        print(f"Source: {metadata['source']}")
        print(f"Document ID: {metadata['document_id']}")
        print(f"Page: {metadata['page']}")
        print(f"Score: {result.score:.4f}")

        assert metadata["document_id"] == document_id
        assert metadata["source"] == expected_filename

    return results


def main():

    print("\n==============================")
    print("MULTI-DOCUMENT ISOLATION TEST")
    print("==============================")

    embedder = Embedder()
    vector_store = VectorStore()

    try:

        # Test 1: Research paper
        test_document(
            vector_store=vector_store,
            embedder=embedder,
            document_id=RESEARCH_DOCUMENT_ID,
            question="What is attention?",
            expected_filename="research_paper.pdf"
        )

        # Test 2: Database document
        test_document(
            vector_store=vector_store,
            embedder=embedder,
            document_id=DATABASE_DOCUMENT_ID,
            question="What is a relational database?",
            expected_filename="database_test.pdf"
        )

        print("\n==============================")
        print("VALIDATION")
        print("==============================")
        print("Research document isolation: PASS")
        print("Database document isolation: PASS")
        print("Multi-document isolation: PASS")
        print("==============================")

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()
