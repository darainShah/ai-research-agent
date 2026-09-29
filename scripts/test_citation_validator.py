from app.evaluation.citation_validator import validate_citations


class FakeResult:

    def __init__(self, page):
        self.payload = {
            "metadata": {
                "page": page
            }
        }


results = [
    FakeResult(page=1),
    FakeResult(page=4),
    FakeResult(page=5),
]


answer = (
    "Attention is important for understanding tokens. "
    "[Source 1, Page 1] "
    "Self-attention is used in LLMs. "
    "[Source 2, Page 99]"
)


result = validate_citations(
    answer=answer,
    results=results
)


print("=" * 40)
print("CITATION VALIDATOR TEST")
print("=" * 40)

print("Citations:", result["citations"])
print("Valid:", result["valid_citations"])
print("Invalid:", result["invalid_citations"])
print("All valid:", result["all_valid"])


if (
    len(result["valid_citations"]) == 1
    and len(result["invalid_citations"]) == 1
    and result["all_valid"] is False
):
    print("\nPASS: Invalid citation detected.")
else:
    print("\nFAIL: Citation validation failed.")