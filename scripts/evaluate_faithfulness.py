from app.rag_pipeline import RAGPipeline


DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)


EVALUATION_QUESTIONS = [
    "What is attention?",
    "What are Q, K, and V?",
    "What is self-attention?",
    "What is the attention score?",
    "What is the formula for self-attention?",
]


def main():

    pipeline = RAGPipeline()

    total = len(EVALUATION_QUESTIONS)
    supported_answers = 0

    print("\n==============================")
    print("FAITHFULNESS EVALUATION")
    print("==============================")

    try:

        for index, question in enumerate(
            EVALUATION_QUESTIONS,
            start=1
        ):

            result = pipeline.answer(
                question=question,
                document_id=DOCUMENT_ID,
                retrieval_k=10,
                final_k=3
            )

            answer = result["answer"]
            citations = result["citation_validation"]

            is_supported = (
                citations["all_valid"]
                and len(result["sources"]) > 0
                and answer
                != "I don't know based on the provided documents."
            )

            if is_supported:
                supported_answers += 1

            print("\n------------------------------")
            print(f"Question {index}/{total}")
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(
                f"Citation validation: "
                f"{citations['all_valid']}"
            )
            print(
                f"Sources found: "
                f"{len(result['sources']) > 0}"
            )
            print(
                f"Faithfulness check: "
                f"{'PASS' if is_supported else 'FAIL'}"
            )

    finally:

        pipeline.close()

    faithfulness_rate = (
        supported_answers / total
        if total > 0
        else 0
    )

    print("\n==============================")
    print("FAITHFULNESS SUMMARY")
    print("==============================")
    print(f"Questions evaluated: {total}")
    print(f"Supported answers: {supported_answers}")
    print(
        f"Faithfulness rate: "
        f"{faithfulness_rate * 100:.2f}%"
    )
    print("==============================")


if __name__ == "__main__":
    main()
