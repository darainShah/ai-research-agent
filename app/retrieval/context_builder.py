def build_context(results):
    context_parts = []

    for i, result in enumerate(results, start=1):
        text = result.payload["text"]
        metadata = result.payload["metadata"]

        source = metadata["source"]
        page = metadata["page"]

        context_part = (
            f"[SOURCE {i}]\n"
            f"Document: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{text}"
        )

        context_parts.append(context_part)

    return "\n\n".join(context_parts)