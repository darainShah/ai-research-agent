import json

from app.rag_pipeline import RAGPipeline


DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)

EXPECTED_REFUSAL = "I don't know based on the provided documents."


def main():
    with open(
        "tests/unanswerable_questions.json",
        "r",
        encoding="utf-8"
    ) as file:
        evaluation_cases = json.load(file)

    pipeline = RAGPipeline()

    total = len(evaluation_cases)
    correct_refusals = 0

    print("\n==============================")
    print("UNANSWERABLE QUESTION EVALUATION")
    print("==============================")

    try:
        for index, case in enumerate(evaluation_cases, start=1):
            question = case["question"]

            result = pipeline.answer(
                question=question,
                document_id=DOCUMENT_ID,
                retrieval_k=10,
                final_k=3
            )

            answer = result["answer"].strip()

            refused = answer == EXPECTED_REFUSAL

            if refused:
                correct_refusals += 1

            print("\n------------------------------")
            print(f"QUESTION {index}/{total}")
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(f"Expected refusal: {EXPECTED_REFUSAL}")
            print(f"Result: {'PASS' if refused else 'FAIL'}")

    finally:
        pipeline.close()

    refusal_rate = (
        correct_refusals / total
        if total > 0
        else 0
    )

    print("\n==============================")
    print("UNANSWERABLE EVALUATION SUMMARY")
    print("==============================")
    print(f"Questions evaluated: {total}")
    print(f"Correct refusals: {correct_refusals}")
    print(f"Refusal rate: {refusal_rate * 100:.2f}%")
    print("==============================")


if __name__ == "__main__":
    main()
