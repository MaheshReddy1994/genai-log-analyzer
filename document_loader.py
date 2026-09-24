from pathlib import Path

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


def chunk_text(text, chunk_size=300, overlap=50):
    """
    Splits the input text into chunks of specified size with a specified overlap.
    
    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of overlapping characters between chunks.
        
    Returns:
        List[str]: A list of text chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")
        
    if overlap < 0  and overlap >= chunk_size:
        raise ValueError("overlap must be a non-negative integer less than chunk_size.")
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start+=chunk_size - overlap  # Move start forward by chunk_size minus overlap
    return chunks

if __name__ == "__main__":
    file_path = KNOWLEDGE_BASE_DIR / "bamboo_troubleshooting.txt"
    
    content = load_document(file_path)
    
    chunks = chunk_text(content, chunk_size=300, overlap=50)
    print (f"Total chunks created: {len(chunks)}")
    
    for index, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {index} ---")

        print(chunk)