from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        score_threshold: float = 0.0
    ):
        self.model = CrossEncoder(model_name)
        self.score_threshold = score_threshold

    def rerank(
        self,
        query: str,
        results: list,
        top_k: int = 3
    ):
        if not results:
            return []

        pairs = [
            (
                query,
                result.payload["text"]
            )
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked_results = sorted(
            zip(results, scores),
            key=lambda x: x[1],
            reverse=True
        )

        reranked_results = []

        for result, score in ranked_results:

            score = float(score)

            # Remove results that the cross-encoder
            # considers insufficiently relevant.
            if score < self.score_threshold:
                continue

            reranked_results.append(
                {
                    "result": result,
                    "reranker_score": score
                }
            )

            if len(reranked_results) >= top_k:
                break

        return reranked_results