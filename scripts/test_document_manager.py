from app.core.document_manager import DocumentManager


def main():

    manager = DocumentManager()

    valid_document_id = "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
    invalid_document_id = "invalid-document-id"

    print("\n==============================")
    print("DOCUMENT EXISTENCE TEST")
    print("==============================")

    valid_result = manager.document_exists(
        valid_document_id
    )

    invalid_result = manager.document_exists(
        invalid_document_id
    )

    print(
        f"Valid document exists: "
        f"{valid_result}"
    )

    print(
        f"Invalid document exists: "
        f"{invalid_result}"
    )

    assert valid_result is True
    assert invalid_result is False

    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    main()