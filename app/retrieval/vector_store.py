from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
import hashlib


class VectorStore:

    def __init__(
        self,
        collection_name="research_documents",
        vector_size=384
    ):
        self.client = QdrantClient(path="data/qdrant")
        self.collection_name = collection_name
        self._create_collection(vector_size)

    def _create_collection(self, vector_size):

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in collection_names:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def _generate_id(self, chunk):

        unique_text = (
            f"{chunk['metadata']['source']}"
            f"_{chunk['metadata']['page']}"
            f"_{chunk['text']}"
        )

        return hashlib.md5(
            unique_text.encode("utf-8")
        ).hexdigest()

    def add_documents(self, chunks, embeddings):

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            point = PointStruct(
                id=self._generate_id(chunk),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "metadata": chunk["metadata"]
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    def search(
        self,
        query_vector,
        limit=5,
        document_id=None
    ):

        query_filter = None

        if document_id:

            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="metadata.document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit
        )

        return results.points


    def delete_document(self, document_id: str):
    
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=query_filter
        )
    def close(self):
        self.client.close()