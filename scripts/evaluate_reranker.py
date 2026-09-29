from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


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


RETRIEVAL_K = 5
FINAL_K = 3


def calculate_reciprocal_rank(
    results,
    relevant_pages
):

    for rank, result in enumerate(
        results,
        start=1
    ):

        page = result.payload[
            "metadata"
        ]["page"]

        if page in relevant_pages:
            return 1 / rank

    return 0


def main():

    retriever = Retriever()
    reranker = Reranker()

    vector_reciprocal_ranks = []
    reranked_reciprocal_ranks = []

    vector_hits = 0
    reranked_hits = 0

    print("\n==============================")
    print("RERANKER EVALUATION")
    print("==============================")


    try:

        for case in EVALUATION_CASES:

            question = case["question"]
            relevant_pages = case[
                "relevant_pages"
            ]


            # ------------------------------------------
            # Vector retrieval
            # ------------------------------------------

            retrieved_results = retriever.retrieve(
                query=question,
                top_k=RETRIEVAL_K,
                document_id=DOCUMENT_ID
            )


            vector_pages = [
                result.payload[
                    "metadata"
                ]["page"]

                for result in retrieved_results
            ]


            vector_hit = any(
                page in relevant_pages
                for page in vector_pages
            )


            if vector_hit:
                vector_hits += 1


            vector_rr = calculate_reciprocal_rank(
                retrieved_results,
                relevant_pages
            )


            vector_reciprocal_ranks.append(
                vector_rr
            )


            # ------------------------------------------
            # Cross-encoder reranking
            # ------------------------------------------

            reranked = reranker.rerank(
                query=question,
                results=retrieved_results,
                top_k=FINAL_K
            )


            reranked_results = [
                item["result"]
                for item in reranked
            ]


            reranked_pages = [
                result.payload[
                    "metadata"
                ]["page"]

                for result in reranked_results
            ]


            reranked_hit = any(
                page in relevant_pages
                for page in reranked_pages
            )


            if reranked_hit:
                reranked_hits += 1


            reranked_rr = calculate_reciprocal_rank(
                reranked_results,
                relevant_pages
            )


            reranked_reciprocal_ranks.append(
                reranked_rr
            )


            # ------------------------------------------
            # Print results
            # ------------------------------------------

            print("\n------------------------------")

            print(
                f"Question: {question}"
            )

            print(
                f"Relevant pages: "
                f"{relevant_pages}"
            )

            print(
                f"Vector pages: "
                f"{vector_pages}"
            )

            print(
                f"Reranked pages: "
                f"{reranked_pages}"
            )

            print(
                f"Vector RR: "
                f"{vector_rr:.3f}"
            )

            print(
                f"Reranked RR: "
                f"{reranked_rr:.3f}"
            )


    finally:

        retriever.close()


    # ------------------------------------------
    # Final metrics
    # ------------------------------------------

    total = len(EVALUATION_CASES)


    vector_hit_rate = (
        vector_hits / total
    )


    reranked_hit_rate = (
        reranked_hits / total
    )


    vector_mrr = (
        sum(vector_reciprocal_ranks)
        / total
    )


    reranked_mrr = (
        sum(reranked_reciprocal_ranks)
        / total
    )


    print("\n==============================")
    print("FINAL METRICS")
    print("==============================")


    print(
        f"Vector Hit@{RETRIEVAL_K}: "
        f"{vector_hit_rate * 100:.1f}%"
    )


    print(
        f"Reranked Hit@{FINAL_K}: "
        f"{reranked_hit_rate * 100:.1f}%"
    )


    print(
        f"Vector MRR: "
        f"{vector_mrr:.3f}"
    )


    print(
        f"Reranked MRR: "
        f"{reranked_mrr:.3f}"
    )


    print(
        f"MRR improvement: "
        f"{reranked_mrr - vector_mrr:+.3f}"
    )


    print("==============================")


if __name__ == "__main__":

    main()

