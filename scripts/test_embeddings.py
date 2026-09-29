from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


sentences = [
    "The model was trained using Indian air quality data.",
    "Indian AQI data was used to train the model.",
    "The weather is sunny today.",
]


embeddings = model.encode(
    sentences,
    normalize_embeddings=True
)


similarity = cosine_similarity(
    embeddings
)


print(similarity)