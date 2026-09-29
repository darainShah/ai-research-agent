from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


def main():

    document_id = "49d44fe8a029d21b653fe6fcbce7c5e0"

    question = "What is attention?"

    print("\n==============================")
    print("METADATA FILTER TEST")
    print("==============================")

    embedder = Embedder()
    vector_store = VectorStore()

    query_vector = embedder.embed_text(question)

    results = vector_store.search(
        query_vector=query_vector,
        limit=5,
        document_id=document_id
    )

    print(
        f"\nRetrieved {len(results)} results"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        metadata = result.payload["metadata"]

        print(
            f"\nResult {index}"
        )

        print(
            f"Document ID: "
            f"{metadata['document_id']}"
        )

        print(
            f"Source: "
            f"{metadata['source']}"
        )

        print(
            f"Page: "
            f"{metadata['page']}"
        )

        print(
            f"Chunk ID: "
            f"{metadata['chunk_id']}"
        )

        print(
            f"Score: "
            f"{result.score:.4f}"
        )

    # Verify every result belongs
    # to the requested document.
    for result in results:

        metadata = result.payload["metadata"]

        assert (
            metadata["document_id"]
            == document_id
    )

    print("\n==============================")
    print("FILTER VALIDATION")
    print("==============================")
    print("All results belong to the requested document.")
    print("Metadata filter: PASS")
    print("==============================")

    vector_store.close()


if __name__ == "__main__":
    main()