from app.retrieval.document_search import DocumentSearch
from app.retrieval.context_builder import build_context
from app.generation.llm import LLM
from app.evaluation.citation_validator import validate_citations


class RAGPipeline:

    def __init__(self, vector_store=None):
        self.document_search = DocumentSearch(
            vector_store=vector_store
        )
        self.llm = LLM()

    def answer(
        self,
        question: str,
        document_id: str,
        chat_history: list = None,
        retrieval_k: int = 10,
        final_k: int = 3,
        retrieval_threshold: float = 0.30
    ):

        if chat_history is None:
            chat_history = []

        # Step 1: Rewrite question
        search_question = self.llm.rewrite_question(
            question=question,
            chat_history=chat_history
        )

        # Step 2: Retrieve relevant chunks
        reranked_results = self.document_search.search(
            question=search_question,
            document_id=document_id,
            retrieval_k=retrieval_k,
            final_k=final_k
        )

        # Step 3: No results
        if not reranked_results:
            return {
                "question": question,
                "answer": (
                    "I don't know based on the "
                    "provided documents."
                ),
                "sources": [],
                "citation_validation": {
                    "citations": [],
                    "valid_citations": [],
                    "invalid_citations": [],
                    "all_valid": True
                }
            }

        # Step 4: Relevance check
        best_vector_score = max(
            item["result"].score
            for item in reranked_results
        )

        if best_vector_score < retrieval_threshold:
            return {
                "question": question,
                "answer": (
                    "I don't know based on the "
                    "provided documents."
                ),
                "sources": [],
                "citation_validation": {
                    "citations": [],
                    "valid_citations": [],
                    "invalid_citations": [],
                    "all_valid": True
                }
            }

        # Step 5: Final results
        final_results = [
            item["result"]
            for item in reranked_results
        ]

        # Step 6: Build context
        context = build_context(
            final_results
        )

        # Step 7: Generate answer
        answer = self.llm.generate(
            question=question,
            context=context,
            chat_history=chat_history
        )

        # Step 8: Validate citations
        citation_validation = validate_citations(
            answer=answer,
            results=final_results
        )

        # Step 9: Return response
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "source": result.payload[
                        "metadata"
                    ]["source"],

                    "page": result.payload[
                        "metadata"
                    ]["page"],

                    "document_id": result.payload[
                        "metadata"
                    ]["document_id"],

                    "chunk_id": result.payload[
                        "metadata"
                    ]["chunk_id"],

                    "vector_score": result.score
                }

                for result in final_results
            ],

            "citation_validation": citation_validation
        }

    def close(self):
        self.document_search.close()