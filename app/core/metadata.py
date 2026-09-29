from pathlib import Path
import hashlib


def generate_document_id(file_path: str) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    sha256 = hashlib.sha256()

    with open(path, "rb") as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_chunk_metadata(
    file_path: str,
    page: int,
    chunk_index: int
):

    document_id = generate_document_id(file_path)

    return {
        "document_id": document_id,
        "source": Path(file_path).name,
        "page": page,
        "chunk_id": (
            f"{document_id}_{page}_{chunk_index}"
        )
    }