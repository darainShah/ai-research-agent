from app.retrieval.document_search import DocumentSearch
from app.core.document import get_document_info


def main():

    pdf_path = "data/raw/research_paper.pdf"

    document_info = get_document_info(pdf_path)
    document_id = document_info["document_id"]

    question = "What is a relational database?"

    print("\n==============================")
    print("DOCUMENT SEARCH TEST")
    print("==============================")

    print(f"Document: {document_info['filename']}")
    print(f"Document ID: {document_id}")
    print(f"Question: {question}")

    search = DocumentSearch()

    try:
        results = search.search(
            question=question,
            document_id=document_id,
            retrieval_k=5,
            final_k=3
        )

        print("\n==============================")
        print("SEARCH RESULTS")
        print("==============================")

        print(f"Results found: {len(results)}")

        for index, item in enumerate(results, start=1):

            result = item["result"]
            reranker_score = item["reranker_score"]

            metadata = result.payload["metadata"]

            print(f"\nResult {index}")
            print(f"Source: {metadata['source']}")
            print(f"Page: {metadata['page']}")
            print(f"Vector Score: {result.score:.4f}")
            print(f"Reranker Score: {reranker_score:.4f}")
            print(f"Text: {result.payload['text']}")

        assert len(results) > 0

        for item in results:
            result = item["result"]
            metadata = result.payload["metadata"]

            assert metadata["document_id"] == document_id

        print("\n==============================")
        print("VALIDATION")
        print("==============================")
        print("Results were retrieved from the correct document.")
        print("Document Search: PASS")
        print("==============================")

    finally:
        search.close()


if __name__ == "__main__":
    main()