from semantic_search import cosine_similarity

class SimpleVectorStore:
    def __init__(self):
        self.documents = []
        
    def add(self, document_id, text, embedding, metadata=None):
        """
        Add a document to the vector store.

        Args:
            document_id (str): Unique identifier for the document.
            text (str): The text content of the document.
            embedding (list): The embedding vector for the document.
            metadata (dict, optional): Additional metadata for the document. Defaults to None.
        """
        document = {
            "document_id": document_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        self.documents.append(document)
        
        
    def search(self, query_embedding, top_k=3):
        """
        Search for the most similar documents to the given query embedding.

        Args:
            query_embedding (list): The embedding vector for the query.
            top_k (int): The number of top similar documents to return.
            """
        results = []
        
        for document in self.documents:
            score = cosine_similarity(query_embedding, document["embedding"])
            results.append({
                "id": document["document_id"],
                "text": document["text"],
                "score": score,
                "metadata": document["metadata"]
            })
            
        results.sort(key = lambda item: item["score"], reverse=True)
            
        return results[:top_k]