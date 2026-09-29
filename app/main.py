
from fastapi import FastAPI

from app.api.document_api import router as document_router
from app.api.question_api import router as question_router
from app.retrieval.vector_store import VectorStore
from app.ingestion.document_ingestor import DocumentIngestor
from app.core.document_manager import DocumentManager
from app.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Research & Document Intelligence Agent",
    version="1.0.0"
)


# --------------------------------------------------
# Shared VectorStore
# --------------------------------------------------

vector_store = VectorStore()

document_manager = DocumentManager(
    vector_store=vector_store
)

document_ingestor = DocumentIngestor(
    vector_store=vector_store
)

rag_pipeline = RAGPipeline(
    vector_store=vector_store
)


# Make shared services available to API routers.
app.state.vector_store = vector_store
app.state.document_manager = document_manager
app.state.document_ingestor = document_ingestor
app.state.rag_pipeline = rag_pipeline


app.include_router(document_router)
app.include_router(question_router)


@app.get("/")
def root():
    return {
        "message": (
            "AI Research & Document Intelligence Agent "
            "API is running."
        )
    }


@app.on_event("shutdown")
def shutdown():
    rag_pipeline.close()
    vector_store.close()
