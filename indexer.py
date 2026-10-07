from document_loader import load_document, chunk_text, KNOWLEDGE_BASE_DIR

from embedding import generate_embedding
from vector_store import SimpleVectorStore

def build_indexer():
    """
    Builds an indexer by loading documents, chunking them, generating embeddings, and storing them in a vector store.

    Returns:
        SimpleVectorStore: An instance of the SimpleVectorStore containing the indexed documents.
    """
    file_path = KNOWLEDGE_BASE_DIR / "bamboo_troubleshooting.txt"
    
    document_content = load_document(file_path)
    chunks = chunk_text(document_content, chunk_size=300, overlap=50)
    store = SimpleVectorStore()
    
    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        store.add(
            document_id = f"bamboo_chunk_{index}",
            text = chunk,
            embedding = embedding,
            metadata = {
                "source": file_path.name,
                "chunk_index": index
            }
        )
    return store


if __name__ == "__main__":
    indexer = build_indexer()
    print(f"Total documents indexed: {len(indexer.documents)}")