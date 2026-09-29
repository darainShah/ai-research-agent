
import hashlib
import logging
import re
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Request
)

from app.api.schemas import DocumentResponse


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def safe_filename(filename: str) -> str:
    """
    Remove unsafe characters from uploaded filenames.
    """
    filename = Path(filename).name

    filename = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename
    )

    return filename


@router.get(
    "/",
    response_model=list[DocumentResponse]
)
async def list_documents(request: Request):

    try:

        document_manager = (
            request.app.state.document_manager
        )

        return document_manager.list_documents(
            str(UPLOAD_DIR)
        )

    except Exception:

        logger.exception(
            "Error while listing documents"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to list documents."
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    request: Request
):

    document_manager = (
        request.app.state.document_manager
    )

    if not document_manager.document_exists(
        document_id
    ):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:

        result = document_manager.delete_document(
            document_id
        )

        return {
            "message": "Document deleted successfully.",
            "document_id": result["document_id"],
            "filename": result["filename"]
        }

    except Exception:

        logger.exception(
            "Error while deleting document: %s",
            document_id
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to delete document."
        )


@router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # Content-based document ID.
        document_id = hashlib.sha256(
            contents
        ).hexdigest()

        document_manager = (
            request.app.state.document_manager
        )

        document_ingestor = (
            request.app.state.document_ingestor
        )

        # Prevent duplicate content.
        existing_documents = (
            document_manager.list_documents(
                str(UPLOAD_DIR)
            )
        )

        if any(
            document["document_id"] == document_id
            for document in existing_documents
        ):

            raise HTTPException(
                status_code=409,
                detail="This document has already been uploaded."
            )

        # Sanitize original filename.
        original_filename = safe_filename(
            file.filename
        )

        # Create unique physical filename.
        stem = Path(
            original_filename
        ).stem

        suffix = Path(
            original_filename
        ).suffix.lower()

        stored_filename = (
            f"{stem}_{document_id[:8]}{suffix}"
        )

        file_path = (
            UPLOAD_DIR / stored_filename
        )

        # Save file.
        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(contents)

        try:

            result = document_ingestor.ingest(
                str(file_path)
            )

        except Exception:

            # Roll back file if indexing fails.
            if file_path.exists():
                file_path.unlink()

            raise

        return {
            "message": (
                "Document uploaded and indexed successfully."
            ),
            "document_id": result["document_id"],
            "filename": result["filename"],
            "pages": result["pages"],
            "chunks": result["chunks"],
            "vectors_stored": result["vectors_stored"]
        }

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Error while uploading document: %s",
            file.filename
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to upload and index document."
        )
