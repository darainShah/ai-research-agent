import re

from app.core.metadata import create_chunk_metadata


def split_into_sentences(text: str):
    return [
        sentence.strip()
        for sentence in re.split(
            r'(?<=[.!?])\s+',
            text
        )
        if sentence.strip()
    ]


def split_oversized_sentence(
    sentence: str,
    chunk_size: int
):
    words = sentence.split()

    chunks = []
    current = ""

    for word in words:

        candidate = (
            word
            if not current
            else current + " " + word
        )

        if len(candidate) <= chunk_size:
            current = candidate

        else:
            if current:
                chunks.append(current)

            # Handle an individual word longer than chunk_size
            if len(word) > chunk_size:
                for i in range(
                    0,
                    len(word),
                    chunk_size
                ):
                    chunks.append(
                        word[i:i + chunk_size]
                    )
                current = ""
            else:
                current = word

    if current:
        chunks.append(current)

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 700,
    chunk_overlap: int = 100
):
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text = text.replace("\r\n", "\n")

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # Detect document title
    title = ""

    if len(lines) > 1:
        first_line = lines[0]

        if (
            not re.match(r"^\d+\.\s+", first_line)
            and len(first_line) <= 120
        ):
            title = first_line
            lines = lines[1:]

    # Detect numbered sections
    sections = []
    current_section = []

    for line in lines:

        if re.match(r"^\d+\.\s+", line):

            if current_section:
                sections.append(
                    " ".join(current_section)
                )

            current_section = [line]

        else:
            current_section.append(line)

    if current_section:
        sections.append(
            " ".join(current_section)
        )

    chunks = []

    for section in sections:

        if title:
            section = f"{title}\n\n{section}"

        if len(section) <= chunk_size:
            chunks.append(section)
            continue

        sentences = split_into_sentences(section)

        # First split oversized sentences
        normalized_sentences = []

        for sentence in sentences:

            if len(sentence) <= chunk_size:
                normalized_sentences.append(sentence)

            else:
                normalized_sentences.extend(
                    split_oversized_sentence(
                        sentence,
                        chunk_size
                    )
                )

        current_sentences = []
        current_length = 0

        for sentence in normalized_sentences:

            sentence_length = len(sentence)

            added_length = (
                sentence_length
                + (1 if current_sentences else 0)
            )

            if (
                current_length + added_length
                <= chunk_size
            ):

                current_sentences.append(sentence)

                current_length += added_length

            else:

                if current_sentences:
                    chunks.append(
                        " ".join(current_sentences)
                    )

                # Preserve sentence-level overlap
                overlap_sentences = []
                overlap_length = 0

                for previous_sentence in reversed(
                    current_sentences
                ):

                    extra_length = (
                        len(previous_sentence)
                        + (
                            1
                            if overlap_sentences
                            else 0
                        )
                    )

                    if (
                        overlap_length
                        + extra_length
                        <= chunk_overlap
                    ):
                        overlap_sentences.insert(
                            0,
                            previous_sentence
                        )

                        overlap_length += extra_length

                    else:
                        break

                current_sentences = (
                    overlap_sentences
                    + [sentence]
                )

                current_length = sum(
                    len(item)
                    for item in current_sentences
                ) + max(
                    0,
                    len(current_sentences) - 1
                )

        if current_sentences:
            chunks.append(
                " ".join(current_sentences)
            )

    return chunks


def create_chunks_with_metadata(
    pages,
    file_path: str
):
    """
    Convert loaded PDF pages into chunks
    with standardized metadata.
    """

    chunks = []

    for page_data in pages:

        page_number = page_data["metadata"]["page"]
        page_text = page_data["text"]

        page_chunks = chunk_text(page_text)

        for chunk_index, chunk in enumerate(
            page_chunks,
            start=1
        ):

            metadata = create_chunk_metadata(
                file_path=file_path,
                page=page_number,
                chunk_index=chunk_index
            )

            chunks.append({
                "text": chunk,
                "metadata": metadata
            })

    return chunks
