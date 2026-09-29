from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


def main():

    embedder = Embedder()
    vector_store = VectorStore()

    print("\n==============================")
    print("MULTI-DOCUMENT TEST")
    print("==============================")

    # ---------------------------------
    # Test 1: Attention document
    # ---------------------------------

    question_1 = "What is attention?"

    vector_1 = embedder.embed_text(question_1)

    results_1 = vector_store.search(
        query_vector=vector_1,
        limit=5
    )

    print("\nQuestion 1:")
    print(question_1)

    print("\nTop results:")

    for result in results_1:

        metadata = result.payload["metadata"]

        print(
            f"Source: {metadata['source']} "
            f"| Page: {metadata['page']} "
            f"| Document ID: {metadata['document_id']} "
            f"| Score: {result.score:.4f}"
        )

    # ---------------------------------
    # Test 2: Database document
    # ---------------------------------

    question_2 = "What is a relational database?"

    vector_2 = embedder.embed_text(question_2)

    results_2 = vector_store.search(
        query_vector=vector_2,
        limit=5
    )

    print("\nQuestion 2:")
    print(question_2)

    print("\nTop results:")

    for result in results_2:

        metadata = result.payload["metadata"]

        print(
            f"Source: {metadata['source']} "
            f"| Page: {metadata['page']} "
            f"| Document ID: {metadata['document_id']} "
            f"| Score: {result.score:.4f}"
        )

    print("\n==============================")
    print("MULTI-DOCUMENT VALIDATION")
    print("==============================")

    document_ids = set()

    for result in results_1 + results_2:

        metadata = result.payload["metadata"]

        document_ids.add(
            metadata["document_id"]
        )

    print(f"Documents found: {len(document_ids)}")

    assert len(document_ids) >= 2

    print("Multiple documents detected.")
    print("Multi-document storage: PASS")

    print("==============================")

    vector_store.close()


if __name__ == "__main__":
    main()