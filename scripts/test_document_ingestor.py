from app.ingestion.document_ingestor import DocumentIngestor


def main():

    pdf_path = "data/raw/research_paper.pdf"

    print("\n==============================")
    print("DOCUMENT INGESTOR TEST")
    print("==============================")

    ingestor = DocumentIngestor()

    try:
        result = ingestor.ingest(pdf_path)

        print(f"Filename: {result['filename']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Pages: {result['pages']}")
        print(f"Chunks: {result['chunks']}")
        print(f"Embeddings: {result['embeddings']}")
        print(f"Vectors stored: {result['vectors_stored']}")

        assert result["pages"] > 0
        assert result["chunks"] > 0
        assert result["embeddings"] > 0
        assert result["vectors_stored"] > 0

        print("\n==============================")
        print("VALIDATION")
        print("==============================")
        print("Document ingestion completed successfully.")
        print("Document Ingestor: PASS")
        print("==============================")

    finally:
        ingestor.close()


if __name__ == "__main__":
    main()