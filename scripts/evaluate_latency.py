import time
import statistics

from app.rag_pipeline import RAGPipeline


DOCUMENT_ID = (
    "87326e24c4d9bea29f6f0fda5565d904b9aed7d4eb6955a91657f70627731ca5"
)


QUESTIONS = [
    "What is attention?",
    "What are Q, K, and V?",
    "What is self-attention?",
    "What is the attention score?",
    "What is the formula for self-attention?",
]


def main():

    pipeline = RAGPipeline()

    latencies = []

    print("\n==============================")
    print("RAG LATENCY EVALUATION")
    print("==============================")

    try:

        for index, question in enumerate(
            QUESTIONS,
            start=1
        ):

            start_time = time.perf_counter()

            result = pipeline.answer(
                question=question,
                document_id=DOCUMENT_ID,
                retrieval_k=10,
                final_k=3
            )

            end_time = time.perf_counter()

            latency = end_time - start_time
            latencies.append(latency)

            print("\n------------------------------")
            print(f"Question {index}/{len(QUESTIONS)}")
            print(f"Question: {question}")
            print(f"Latency: {latency:.3f} seconds")
            print(
                f"Answer generated: "
                f"{bool(result['answer'])}"
            )

    finally:

        pipeline.close()

    print("\n==============================")
    print("LATENCY SUMMARY")
    print("==============================")

    print(f"Questions evaluated: {len(latencies)}")
    print(
        f"Average latency: "
        f"{statistics.mean(latencies):.3f} seconds"
    )
    print(
        f"Minimum latency: "
        f"{min(latencies):.3f} seconds"
    )
    print(
        f"Maximum latency: "
        f"{max(latencies):.3f} seconds"
    )

    if len(latencies) >= 2:
        print(
            f"Median latency: "
            f"{statistics.median(latencies):.3f} seconds"
        )

    print("==============================")


if __name__ == "__main__":
    main()
