from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


class DocumentSearch:

    def __init__(self, vector_store=None):
        self.retriever = Retriever(
            vector_store=vector_store
        )
        self.reranker = Reranker()

    def search(
        self,
        question: str,
        document_id: str,
        retrieval_k: int = 5,
        final_k: int = 3
    ):
        # Step 1: Dense retrieval
        results = self.retriever.retrieve(
            query=question,
            top_k=retrieval_k,
            document_id=document_id
        )

        # Step 2: Reranking
        reranked_results = self.reranker.rerank(
            query=question,
            results=results,
            top_k=final_k
        )

        return reranked_results

    def close(self):
        self.retriever.close()