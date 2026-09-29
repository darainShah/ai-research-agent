import json

from app.retrieval.retriever import Retriever


def load_questions():
    with open(
        "tests/evaluation_questions.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def evaluate_retrieval():

    questions = load_questions()

    retriever = Retriever()

    top_1_correct = 0
    top_3_correct = 0
    top_5_correct = 0

    print("\n==============================")
    print("RETRIEVAL EVALUATION")
    print("==============================")

    for item in questions:

        question = item["question"]
        expected_pages = item["expected_pages"]

        results = retriever.retrieve(
            query=question,
            top_k=5
        )

        retrieved_pages = [
            result.payload["metadata"]["page"]
            for result in results
        ]

        top_1_pages = retrieved_pages[:1]
        top_3_pages = retrieved_pages[:3]
        top_5_pages = retrieved_pages[:5]

        top_1 = any(
            page in expected_pages
            for page in top_1_pages
        )

        top_3 = any(
            page in expected_pages
            for page in top_3_pages
        )

        top_5 = any(
            page in expected_pages
            for page in top_5_pages
        )

        if top_1:
            top_1_correct += 1

        if top_3:
            top_3_correct += 1

        if top_5:
            top_5_correct += 1

        print("\n------------------------------")
        print(f"Question: {question}")
        print(f"Expected pages: {expected_pages}")
        print(f"Retrieved pages: {retrieved_pages}")

        print(
            f"Top-1: "
            f"{'PASS' if top_1 else 'FAIL'}"
        )

        print(
            f"Top-3: "
            f"{'PASS' if top_3 else 'FAIL'}"
        )

        print(
            f"Top-5: "
            f"{'PASS' if top_5 else 'FAIL'}"
        )

    total = len(questions)

    print("\n==============================")
    print("FINAL METRICS")
    print("==============================")

    print(
        f"Top-1 Accuracy: "
        f"{top_1_correct / total:.2%}"
    )

    print(
        f"Top-3 Accuracy: "
        f"{top_3_correct / total:.2%}"
    )

    print(
        f"Top-5 Accuracy: "
        f"{top_5_correct / total:.2%}"
    )

    retriever.close()


if __name__ == "__main__":
    evaluate_retrieval()