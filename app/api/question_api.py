
import logging

from fastapi import (
    APIRouter,
    HTTPException,
    Request
)

from app.api.schemas import (
    QuestionRequest,
    QuestionResponse
)


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Questions"]
)


@router.post(
    "/{document_id}/ask",
    response_model=QuestionResponse
)
async def ask_question(
    document_id: str,
    request: QuestionRequest,
    http_request: Request
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    document_manager = (
        http_request.app.state.document_manager
    )

    rag_pipeline = (
        http_request.app.state.rag_pipeline
    )

    if not document_manager.document_exists(
        document_id
    ):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:

        chat_history = [
            {
                "role": message.role,
                "content": message.content
            }

            for message in request.chat_history
        ]

        response = rag_pipeline.answer(
            question=request.question,
            document_id=document_id,
            chat_history=chat_history,
            retrieval_k=10,
            final_k=3
        )

        return response

    except Exception:

        logger.exception(
            "Error while answering question "
            "for document_id=%s",
            document_id
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate an answer."
        )
