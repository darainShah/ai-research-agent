from app.retrieval.retriever import Retriever


DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)


EVALUATION_CASES = [
    {
        "question": "What is attention?",
        "relevant_pages": [1],
    },
    {
        "question": "What are Q, K, and V?",
        "relevant_pages": [1, 2, 3, 5],
    },
    {
        "question": "What is self-attention?",
        "relevant_pages": [3, 4],
    },
    {
        "question": "What is the attention score?",
        "relevant_pages": [2],
    },
    {
        "question": "What is the formula for self-attention?",
        "relevant_pages": [3],
    },
]


TOP_K = 5


def main():

    retriever = Retriever()

    total_hits = 0
    reciprocal_ranks = []

    print("\n==============================")
    print("RETRIEVAL EVALUATION")
    print("==============================")

    try:

        for case in EVALUATION_CASES:

            question = case["question"]
            relevant_pages = case["relevant_pages"]

            results = retriever.retrieve(
                query=question,
                top_k=TOP_K,
                document_id=DOCUMENT_ID
            )

            retrieved_pages = [
                result.payload["metadata"]["page"]
                for result in results
            ]

            hit = any(
                page in relevant_pages
                for page in retrieved_pages
            )

            if hit:
                total_hits += 1

            reciprocal_rank = 0

            for rank, page in enumerate(
                retrieved_pages,
                start=1
            ):

                if page in relevant_pages:

                    reciprocal_rank = 1 / rank

                    break

            reciprocal_ranks.append(
                reciprocal_rank
            )

            print("\n------------------------------")

            print(
                f"Question: {question}"
            )

            print(
                f"Expected pages: "
                f"{relevant_pages}"
            )

            print(
                f"Retrieved pages: "
                f"{retrieved_pages}"
            )

            print(
                f"Hit@{TOP_K}: "
                f"{'PASS' if hit else 'FAIL'}"
            )

            print(
                f"Reciprocal Rank: "
                f"{reciprocal_rank:.3f}"
            )

    finally:

        retriever.close()


    hit_rate = (
        total_hits
        / len(EVALUATION_CASES)
    )

    mrr = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
    )


    print("\n==============================")
    print("FINAL METRICS")
    print("==============================")

    print(
        f"Hit@{TOP_K}: "
        f"{hit_rate * 100:.1f}%"
    )

    print(
        f"MRR: "
        f"{mrr:.3f}"
    )

    print("==============================")


if __name__ == "__main__":

    main()