from app.retrieval.vector_store import VectorStore


def main():

    vector_store = VectorStore()

    print("\n==============================")
    print("QDRANT METADATA TEST")
    print("==============================")

    results = vector_store.client.scroll(
        collection_name=vector_store.collection_name,
        limit=5,
        with_payload=True,
        with_vectors=False
    )

    points = results[0]

    print(f"\nRetrieved {len(points)} points\n")

    for index, point in enumerate(points, start=1):

        metadata = point.payload["metadata"]

        print(f"Point {index}")
        print(f"ID: {point.id}")
        print(f"Document ID: {metadata['document_id']}")
        print(f"Source: {metadata['source']}")
        print(f"Page: {metadata['page']}")
        print(f"Chunk ID: {metadata['chunk_id']}")
        print("-" * 40)

    vector_store.close()


if __name__ == "__main__":
    main()