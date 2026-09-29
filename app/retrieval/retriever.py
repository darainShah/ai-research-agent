from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


class Retriever:

    def __init__(self, vector_store=None):
        self.embedder = Embedder()

        if vector_store is None:
            self.vector_store = VectorStore()
            self._owns_vector_store = True
        else:
            self.vector_store = vector_store
            self._owns_vector_store = False

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.25,
        document_id: str = None
    ):
        query_vector = self.embedder.embed_text(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=top_k,
            document_id=document_id
        )

        filtered_results = [
            result
            for result in results
            if result.score >= score_threshold
        ]

        return filtered_results

    def close(self):
        if self._owns_vector_store:
            self.vector_store.close()