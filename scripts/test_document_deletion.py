from pathlib import Path

from app.core.document_manager import DocumentManager
from app.retrieval.vector_store import VectorStore


PDF_PATH = "data/raw/database_test.pdf"

DOCUMENT_ID = (
    "f60d4e3be23fddcc8e61a28b10465e7fb9b53e1348d7a0640ac2090365bb9519"
)


def main():

    print("\n==============================")
    print("DOCUMENT DELETION TEST")
    print("==============================")

    manager = DocumentManager()

    # Step 1: Confirm document exists
    print("\nStep 1: Checking document exists...")

    assert manager.document_exists(DOCUMENT_ID)

    print("Document exists: PASS")

    # Step 2: Delete document
    print("\nStep 2: Deleting document...")

    result = manager.delete_document(DOCUMENT_ID)

    print(f"Deleted filename: {result['filename']}")
    print(f"Deleted document ID: {result['document_id']}")

    assert result["document_id"] == DOCUMENT_ID

    print("Document deletion: PASS")

    # Step 3: Verify physical file is gone
    print("\nStep 3: Checking physical file...")

    assert not Path(PDF_PATH).exists()

    print("Physical file removed: PASS")

    # Step 4: Verify document no longer exists
    print("\nStep 4: Checking document registry...")

    assert not manager.document_exists(DOCUMENT_ID)

    print("Document no longer exists: PASS")

    # Step 5: Verify vectors are gone
    print("\nStep 5: Checking vector database...")

    vector_store = VectorStore()

    try:
        remaining_vectors = vector_store.search(
            query_vector=[0.0] * 384,
            limit=10,
            document_id=DOCUMENT_ID
        )

        print(
            f"Remaining vectors for document: "
            f"{len(remaining_vectors)}"
        )

        assert len(remaining_vectors) == 0

    finally:
        vector_store.close()

    print("Vectors removed: PASS")

    print("\n==============================")
    print("VALIDATION")
    print("==============================")
    print("Document deletion lifecycle: PASS")
    print("==============================")


if __name__ == "__main__":
    main()
