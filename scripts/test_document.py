from app.core.document import get_document_info


def main():

    file_path = "data/raw/research_paper.pdf"

    document = get_document_info(file_path)

    print("\n==============================")
    print("DOCUMENT REGISTRY TEST")
    print("==============================")

    print(f"Filename: {document['filename']}")
    print(f"Document ID: {document['document_id']}")
    print(f"File Path: {document['file_path']}")

    assert document["filename"] == "research_paper.pdf"

    assert document["document_id"] == (
        "49d44fe8a029d21b653fe6fcbce7c5e0"
    )

    print("\nDocument registry: PASS")

    print("==============================")

    
if __name__ == "__main__":
    main()