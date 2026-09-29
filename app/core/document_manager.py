from pathlib import Path

from app.core.document import get_document_info
from app.retrieval.vector_store import VectorStore


class DocumentManager:

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def get_document(self, file_path: str):
        return get_document_info(file_path)

    def list_documents(self, directory: str):
        directory_path = Path(directory)

        if not directory_path.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        documents = []

        for file_path in sorted(directory_path.glob("*.pdf")):
            documents.append(
                get_document_info(str(file_path))
            )

        return documents

    def document_exists(
        self,
        document_id: str,
        directory: str = "data/raw"
    ):
        documents = self.list_documents(directory)

        for document in documents:
            if document["document_id"] == document_id:
                return True

        return False

    def delete_document(
        self,
        document_id: str,
        directory: str = "data/raw"
    ):
        documents = self.list_documents(directory)

        document = None

        for item in documents:
            if item["document_id"] == document_id:
                document = item
                break

        if document is None:
            raise FileNotFoundError(
                f"Document not found: {document_id}"
            )

        # Delete vectors using the shared VectorStore.
        self.vector_store.delete_document(document_id)

        # Delete the actual PDF.
        file_path = Path(document["file_path"])
        file_path.unlink()

        return {
            "document_id": document_id,
            "filename": document["filename"]
        }
from pathlib import Path

from app.core.document import get_document_info
from app.retrieval.vector_store import VectorStore


class DocumentManager:

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def get_document(self, file_path: str):
        return get_document_info(file_path)

    def list_documents(self, directory: str):
        directory_path = Path(directory)

        if not directory_path.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        documents = []

        for file_path in sorted(directory_path.glob("*.pdf")):
            documents.append(
                get_document_info(str(file_path))
            )

        return documents

    def document_exists(
        self,
        document_id: str,
        directory: str = "data/raw"
    ):
        documents = self.list_documents(directory)

        for document in documents:
            if document["document_id"] == document_id:
                return True

        return False

    def delete_document(
        self,
        document_id: str,
        directory: str = "data/raw"
    ):
        documents = self.list_documents(directory)

        document = None

        for item in documents:
            if item["document_id"] == document_id:
                document = item
                break

        if document is None:
            raise FileNotFoundError(
                f"Document not found: {document_id}"
            )

        # Delete vectors using the shared VectorStore.
        self.vector_store.delete_document(document_id)

        # Delete the actual PDF.
        file_path = Path(document["file_path"])
        file_path.unlink()

        return {
            "document_id": document_id,
            "filename": document["filename"]
        }