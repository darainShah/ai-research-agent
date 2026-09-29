from app.retrieval.retriever import Retriever


def main():

    document_id = "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"

    question = "What is attention?"

    print("\n==============================")
    print("RETRIEVER METADATA FILTER TEST")
    print("==============================")

    retriever = Retriever()

    try:

        results = retriever.retrieve(
            query=question,
            top_k=5,
            document_id=document_id
        )

        print(f"\nRetrieved {len(results)} results")

        for index, result in enumerate(results, start=1):

            metadata = result.payload["metadata"]

            print(f"\nResult {index}")
            print(f"Document ID: {metadata['document_id']}")
            print(f"Source: {metadata['source']}")
            print(f"Page: {metadata['page']}")
            print(f"Chunk ID: {metadata['chunk_id']}")
            print(f"Score: {result.score:.4f}")

            assert metadata["document_id"] == document_id

        print("\n==============================")
        print("VALIDATION")
        print("==============================")
        print("All retrieved results belong to the requested document.")
        print("Retriever metadata filter: PASS")
        print("==============================")

    finally:
        retriever.close()


if __name__ == "__main__":
    main()