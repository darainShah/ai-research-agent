import sys

from app.rag_pipeline import RAGPipeline
from app.core.document import get_document_info


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python -m scripts.test_rag <pdf_path>"
        )
        sys.exit(1)

    pdf_path = sys.argv[1]

    document_info = get_document_info(pdf_path)
    document_id = document_info["document_id"]

    print("\n==============================")
    print("DOCUMENT-SPECIFIC RAG TEST")
    print("==============================")

    print(f"Document: {document_info['filename']}")
    print(f"Document ID: {document_id}")

    pipeline = RAGPipeline()

    try:

        question = input("\nEnter your question: ")

        response = pipeline.answer(
            question=question,
            document_id=document_id,
            retrieval_k=5,
            final_k=3
        )

        print("\n==============================")
        print("RETRIEVED CONTEXT")
        print("==============================")

        for source in response["sources"]:
            print(
                f"Source: {source['source']} "
                f"| Page: {source['page']} "
                f"| Score: {source['vector_score']:.4f}"
            )

        print("\n==============================")
        print("ANSWER")
        print("==============================")

        print(response["answer"])

        print("\n==============================")
        print("SOURCES")
        print("==============================")

        for source in response["sources"]:
            print(
                f"Source: {source['source']} "
                f"| Page: {source['page']} "
                f"| Document ID: {source['document_id']} "
                f"| Chunk ID: {source['chunk_id']} "
                f"| Score: {source['vector_score']:.4f}"
            )

        print("\n==============================")
        print("CITATION VALIDATION")
        print("==============================")

        citation_validation = response["citation_validation"]

        print(
            f"All citations valid: "
            f"{citation_validation['all_valid']}"
        )

        print(
            f"Valid citations: "
            f"{citation_validation['valid_citations']}"
        )

        print(
            f"Invalid citations: "
            f"{citation_validation['invalid_citations']}"
        )

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()