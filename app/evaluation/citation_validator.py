import re


def extract_citations(answer: str):
    """
    Extract citations in the format:

    [Source 1, Page 5]
    [Source 2, Page 3]
    """

    pattern = r"\[Source\s+(\d+),\s*Page\s+(\d+)\]"

    matches = re.findall(pattern, 
                         answer,
                         re.IGNORECASE
                         )

    citations = []

    for source_number, page_number in matches:
        citations.append({
            "source": int(source_number),
            "page": int(page_number)
        })

    return citations


def validate_citations(answer: str, results: list):
    """
    Validate citations against the actual retrieved results.
    """

    citations = extract_citations(answer)

    valid_citations = []
    invalid_citations = []

    for citation in citations:

        source_number = citation["source"]
        page_number = citation["page"]

        source_index = source_number - 1

        if source_index < 0 or source_index >= len(results):
            invalid_citations.append(citation)
            continue

        result = results[source_index]

        actual_page = result.payload["metadata"]["page"]

        if actual_page == page_number:
            valid_citations.append(citation)
        else:
            invalid_citations.append(citation)

    return {
        "citations": citations,
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations,
        "all_valid": len(invalid_citations) == 0
    }