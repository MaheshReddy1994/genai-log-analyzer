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
    Keep each troubleshooting section together when possible.
    Split oversized sections into paragraph-based chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size"
        )

    # Split before headings such as "Section 1:"
    sections = re.split(r"(?=Section \d+:)", text.strip())

    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Keep a complete section together if it fits.
        if len(section) <= chunk_size:
            chunks.append(section)
            continue

        # If a section is too long, split it at paragraph boundaries.
        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", section)
            if p.strip()
        ]

        current = ""

        for paragraph in paragraphs:
            candidate = (
                f"{current}\n\n{paragraph}"
                if current else paragraph
            )

            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = paragraph

        if current:
            chunks.append(current)

    return chunks

if __name__ == "__main__":
    file_path = KNOWLEDGE_BASE_DIR / "bamboo_troubleshooting.txt"
    
    content = load_document(file_path)
    
    chunks = chunk_text(content, chunk_size=300, overlap=50)
    print (f"Total chunks created: {len(chunks)}")
    
    for index, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {index} ---")

        print(chunk)