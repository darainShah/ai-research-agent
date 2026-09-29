from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):

    role: str = Field(
        ...,
        description="Message role: user or assistant."
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Message content."
    )

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:

        allowed_roles = {
            "user",
            "assistant"
        }

        if value not in allowed_roles:
            raise ValueError(
                "Role must be 'user' or 'assistant'."
            )

        return value


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the document."
    )

    chat_history: list[ChatMessage] = Field(
        default_factory=list,
        description="Previous conversation messages."
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        if not value.strip():

            raise ValueError(
                "Question cannot be empty or whitespace."
            )

        return value


class SourceResponse(BaseModel):

    source: str
    page: int
    document_id: str
    chunk_id: str
    vector_score: float


class CitationValidationResponse(BaseModel):

    citations: list[dict]
    valid_citations: list[dict]
    invalid_citations: list[dict]
    all_valid: bool


class QuestionResponse(BaseModel):

    question: str
    answer: str
    sources: list[SourceResponse]
    citation_validation: CitationValidationResponse


class DocumentResponse(BaseModel):

    document_id: str
    filename: str