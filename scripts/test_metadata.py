from app.core.metadata import (
    generate_document_id,
    create_chunk_metadata
)


def main():

    file_path = "data/raw/research_paper.pdf"

    document_id = generate_document_id(
        file_path
    )

    print("\n==============================")
    print("METADATA TEST")
    print("==============================")

    print(f"Document ID: {document_id}")

    metadata = create_chunk_metadata(
        file_path=file_path,
        page=5,
        chunk_index=2
    )

    print("\nChunk metadata:")
    print(metadata)

    assert metadata["document_id"] == document_id
    assert metadata["source"] == "research_paper.pdf"
    assert metadata["page"] == 5
    assert metadata["chunk_id"] == f"{document_id}_5_2"

    print("\n==============================")
    print("ALL METADATA TESTS PASSED")
    print("==============================")


if __name__ == "__main__":
    main()