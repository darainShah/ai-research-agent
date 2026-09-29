from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_text


pages = load_pdf(
    "data/raw/research_paper.pdf"
)

all_chunks = []

for page in pages:

    chunks = chunk_text(
        page["text"],
        chunk_size=400,
        chunk_overlap=80
    )

    for chunk in chunks:

        all_chunks.append({
            "text": chunk,
            "metadata": page["metadata"]
        })


print("Number of pages:", len(pages))
print("Number of chunks:", len(all_chunks))


for i, chunk in enumerate(all_chunks[:3]):

    print("\n==============================")
    print("CHUNK:", i + 1)
    print("SOURCE:", chunk["metadata"]["source"])
    print("PAGE:", chunk["metadata"]["page"])
    print("==============================")

    print(chunk["text"])