from pathlib import Path

from app.core.metadata import generate_document_id


def get_document_info(file_path: str):
    """
    Return standardized information about a document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    document_id = generate_document_id(file_path)

    return {
        "document_id": document_id,
        "filename": path.name,
        "file_path": str(path)
    }