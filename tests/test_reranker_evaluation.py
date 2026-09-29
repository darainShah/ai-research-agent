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


def evaluate_reranking():

    questions = load_questions()

    retriever = Retriever()
    reranker = Reranker()

    top_1_correct = 0
    top_3_correct = 0

    print("\n==============================")
    print("RERANKER EVALUATION")
    print("==============================")

    for item in questions:

        question = item["question"]
        expected_pages = item["expected_pages"]

        # ----------------------------
        # Step 1: Retrieve candidates
        # ----------------------------

        results = retriever.retrieve(
            query=question,
            top_k=5
        )

        # ----------------------------
        # Step 2: Rerank candidates
        # ----------------------------

        reranked_results = reranker.rerank(
            query=question,
            results=results,
            top_k=5
        )

        retrieved_pages = [
            item["result"].payload["metadata"]["page"]
            for item in reranked_results
        ]

        # ----------------------------
        # Step 3: Evaluate
        # ----------------------------

        top_1 = any(
            page in expected_pages
            for page in retrieved_pages[:1]
        )

        top_3 = any(
            page in expected_pages
            for page in retrieved_pages[:3]
        )

        if top_1:
            top_1_correct += 1

        if top_3:
            top_3_correct += 1

        print("\n------------------------------")
        print(f"Question: {question}")
        print(f"Expected pages: {expected_pages}")
        print(f"Reranked pages: {retrieved_pages}")

        print(
            f"Top-1: "
            f"{'PASS' if top_1 else 'FAIL'}"
        )

        print(
            f"Top-3: "
            f"{'PASS' if top_3 else 'FAIL'}"
        )

    total = len(questions)

    print("\n==============================")
    print("FINAL RERANKER METRICS")
    print("==============================")

    print(
        f"Top-1 Accuracy: "
        f"{top_1_correct / total:.2%}"
    )

    print(
        f"Top-3 Accuracy: "
        f"{top_3_correct / total:.2%}"
    )

    retriever.close()


if __name__ == "__main__":
    evaluate_reranking()
