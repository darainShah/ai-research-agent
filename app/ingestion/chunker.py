def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """
    Split text into overlapping chunks.

    Parameters
    ----------
    text : str
        Input document text.

    chunk_size : int
        Approximate maximum number of characters per chunk.

    chunk_overlap : int
        Number of characters shared between consecutive chunks.

    Returns
    -------
    list[str]
        List of text chunks.
    """

    if not text:
        return []

    text = " ".join(text.split())

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - chunk_overlap

    return chunks