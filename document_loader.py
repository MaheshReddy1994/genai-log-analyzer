from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

print(f"knowledge_base_dir: {KNOWLEDGE_BASE_DIR}")

def load_document(file_path):
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    return file_path.read_text(encoding="utf-8",errors="replace")






def chunk_text(text, chunk_size=500, overlap=50):
    """
    Keep sections together when possible.
    Split oversized sections at paragraph boundaries.
    Reuse complete paragraphs as overlap where possible.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size"
        )

    sections = re.split(r"(?=Section \d+:)", text.strip())
    chunks = []

    for section in sections:
        section = section.strip()
        print(f"Section length: {len(section)}")
        print(f"Section starts: {section[:50]!r}")
        if not section:
            continue

        if len(section) <= chunk_size:
            chunks.append(section)
            continue

        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", section)
            if p.strip()
        ]

        current_paragraphs = []

        for paragraph in paragraphs:
            candidate_paragraphs = current_paragraphs + [paragraph]
            candidate = "\n\n".join(candidate_paragraphs)

            if len(candidate) <= chunk_size:
                current_paragraphs = candidate_paragraphs
                continue

            if current_paragraphs:
                chunks.append("\n\n".join(current_paragraphs))

            # Reuse whole trailing paragraphs where possible.
            overlap_paragraphs = []
            overlap_length = 0

            for previous in reversed(current_paragraphs):
                extra_length = len(previous) + (
                    2 if overlap_paragraphs else 0
                )

                if overlap_length + extra_length > overlap:
                    break

                overlap_paragraphs.insert(0, previous)
                overlap_length += extra_length

            current_paragraphs = overlap_paragraphs + [paragraph]

            # If overlap plus the new paragraph is too large,
            # keep the new paragraph alone.
            if len("\n\n".join(current_paragraphs)) > chunk_size:
                current_paragraphs = [paragraph]

        if current_paragraphs:
            chunks.append("\n\n".join(current_paragraphs))

    return chunks


if __name__ == "__main__":
    file_path = KNOWLEDGE_BASE_DIR / "bamboo_troubleshooting.txt"
    
    content = load_document(file_path)
    
    chunks = chunk_text(content, chunk_size=300, overlap=50)
    print (f"Total chunks created: {len(chunks)}")
    
    for index, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {index} ---")

        print(chunk)