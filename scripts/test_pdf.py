from app.ingestion.pdf_loader import load_pdf


pages = load_pdf(
    "data/raw/research_paper.pdf"
)

print(f"Number of pages: {len(pages)}")

for page in pages[:2]:

    print("\n--------------------")

    print("Source:", page["metadata"]["source"])
    print("Page:", page["metadata"]["page"])

    print("\nText:")
    print(page["text"][:500])