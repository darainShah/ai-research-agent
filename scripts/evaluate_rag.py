import json

from app.rag_pipeline import RAGPipeline


EVALUATION_FILE = "tests/evaluation_questions.json"

DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)


def load_questions():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def evaluate_answer(
    answer: str,
    expected_keywords: list[str]
):

    answer_lower = answer.lower()

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    missing_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() not in answer_lower
    ]

    keyword_score = (
        len(matched_keywords)
        / len(expected_keywords)
        if expected_keywords
        else 0
    )

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "keyword_score": keyword_score
    }


def main():

    questions = load_questions()

    pipeline = RAGPipeline()

    results = []

    try:

        for index, item in enumerate(
            questions,
            start=1
        ):

            question = item["question"]

            expected_keywords = item[
                "expected_keywords"
            ]

            print("\n" + "=" * 70)

            print(
                f"QUESTION {index}/{len(questions)}"
            )

            print(
                f"Question: {question}"
            )

            response = pipeline.answer(
                question=question,
                document_id=DOCUMENT_ID,
                chat_history=[],
                retrieval_k=10,
                final_k=3
            )

            answer = response["answer"]

            evaluation = evaluate_answer(
                answer=answer,
                expected_keywords=expected_keywords
            )

            citation_validation = response[
                "citation_validation"
            ]

            has_sources = bool(
                response["sources"]
            )

            print(
                f"\nAnswer:\n{answer}"
            )

            print(
                f"\nExpected keywords:"
            )

            print(
                expected_keywords
            )

            print(
                f"Matched keywords:"
            )

            print(
                evaluation["matched_keywords"]
            )

            print(
                f"Missing keywords:"
            )

            print(
                evaluation["missing_keywords"]
            )

            print(
                f"Keyword score: "
                f"{evaluation['keyword_score']:.2f}"
            )

            print(
                f"Citations valid: "
                f"{citation_validation['all_valid']}"
            )

            print(
                f"Sources found: "
                f"{has_sources}"
            )

            results.append(
                {
                    "question": question,
                    "answer": answer,
                    "keyword_score": evaluation[
                        "keyword_score"
                    ],
                    "matched_keywords": evaluation[
                        "matched_keywords"
                    ],
                    "missing_keywords": evaluation[
                        "missing_keywords"
                    ],
                    "citations_valid": citation_validation[
                        "all_valid"
                    ],
                    "has_sources": has_sources
                }
            )

    finally:

        pipeline.close()


    # --------------------------------------------------
    # Overall Metrics
    # --------------------------------------------------

    total_questions = len(results)

    average_keyword_score = (
        sum(
            result["keyword_score"]
            for result in results
        )
        / total_questions
        if total_questions
        else 0
    )

    citation_success_rate = (
        sum(
            result["citations_valid"]
            for result in results
        )
        / total_questions
        if total_questions
        else 0
    )

    source_rate = (
        sum(
            result["has_sources"]
            for result in results
        )
        / total_questions
        if total_questions
        else 0
    )


    print("\n" + "=" * 70)

    print("RAG EVALUATION SUMMARY")

    print("=" * 70)

    print(
        f"Questions evaluated: "
        f"{total_questions}"
    )

    print(
        f"Average keyword score: "
        f"{average_keyword_score:.2%}"
    )

    print(
        f"Citation validation rate: "
        f"{citation_success_rate:.2%}"
    )

    print(
        f"Source retrieval rate: "
        f"{source_rate:.2%}"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()