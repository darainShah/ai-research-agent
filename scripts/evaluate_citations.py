import json

from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


def load_questions():
    with open(
        "tests/evaluation_questions.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def evaluate_citations():

    questions = load_questions()

    retriever = Retriever()
    reranker = Reranker()

    citation_correct = 0

    print("\n==============================")
    print("CITATION EVALUATION")
    print("==============================")

    for index, item in enumerate(
        questions,
        start=1
    ):

        question = item["question"]
        expected_pages = item["expected_pages"]

        results = retriever.retrieve(
            query=question,
            top_k=5
        )

        reranked_results = reranker.rerank(
            query=question,
            results=results,
            top_k=3
        )

        retrieved_pages = [
            item["result"]
            .payload["metadata"]["page"]
            for item in reranked_results
        ]

        citation_pass = any(
            page in expected_pages
            for page in retrieved_pages
        )

        if citation_pass:
            citation_correct += 1

        print("\n------------------------------")
        print(f"Question {index}: {question}")
        print("------------------------------")

        print(
            f"Expected pages: {expected_pages}"
        )

        print(
            f"Retrieved pages: {retrieved_pages}"
        )

        print(
            f"Citation: "
            f"{'PASS' if citation_pass else 'FAIL'}"
        )

    total = len(questions)

    citation_accuracy = (
        citation_correct / total
        if total > 0
        else 0
    )

    print("\n==============================")
    print("FINAL CITATION METRICS")
    print("==============================")

    print(
        f"Citation Accuracy: "
        f"{citation_accuracy:.2%}"
    )

    retriever.close()


if __name__ == "__main__":
    evaluate_citations()