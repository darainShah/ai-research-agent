from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_text
from app.core.metadata import create_chunk_metadata
from app.core.document import get_document_info
from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


class DocumentIngestor:

    def __init__(self, vector_store=None):
        self.embedder = Embedder()

        if vector_store is None:
            self.vector_store = VectorStore()
            self._owns_vector_store = True
        else:
            self.vector_store = vector_store
            self._owns_vector_store = False

    def ingest(self, file_path: str):

        # 1. Get document information
        document_info = get_document_info(file_path)

        # Remove previously indexed vectors for this document.
        self.vector_store.delete_document(
            document_info["document_id"]
        )

        # 2. Load PDF
        pages = load_pdf(file_path)

        # 3. Create chunks with metadata
        chunks = []

        for page in pages:

            page_chunks = chunk_text(
                page["text"],
                chunk_size=400,
                chunk_overlap=80
            )

            for chunk_index, chunk in enumerate(
                page_chunks,
                start=1
            ):

                metadata = create_chunk_metadata(
                    file_path=file_path,
                    page=page["metadata"]["page"],
                    chunk_index=chunk_index
                )

                chunks.append({
                    "text": chunk,
                    "metadata": metadata
                })

        # 4. Create embeddings
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedder.embed_documents(texts)

        # 5. Store vectors
        count = self.vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "document_id": document_info["document_id"],
            "filename": document_info["filename"],
            "pages": len(pages),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
            "vectors_stored": count
        }

    def close(self):
        if self._owns_vector_store:
            self.vector_store.close()