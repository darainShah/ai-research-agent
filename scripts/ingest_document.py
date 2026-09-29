import sys

from app.ingestion.document_ingestor import DocumentIngestor


def main():

    if len(sys.argv) != 2:
        print("Usage: python -m scripts.ingest_document <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    print("\n==============================")
    print("DOCUMENT INGESTION")
    print("==============================")
    print(f"File: {pdf_path}")

    ingestor = DocumentIngestor()

    try:
        result = ingestor.ingest(pdf_path)

        print("\nIngestion Results")
        print("------------------------------")
        print(f"Filename: {result['filename']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Pages: {result['pages']}")
        print(f"Chunks: {result['chunks']}")
        print(f"Embeddings: {result['embeddings']}")
        print(f"Vectors stored: {result['vectors_stored']}")

        print("\n==============================")
        print("INGESTION COMPLETE")
        print("==============================")

    finally:
        ingestor.close()


if __name__ == "__main__":
    main()