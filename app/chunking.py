def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:

    clean_text = " ".join(text.split())

    if not clean_text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end]
        chunks.append(chunk)

        if end >= len(clean_text):
            break

        start = end - overlap

    return chunks
