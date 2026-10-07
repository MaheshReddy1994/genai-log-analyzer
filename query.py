from embedding import generate_embedding
from indexer import build_indexer

def search_knowledge_base(query, top_k=3):
    """
    Searches the knowledge base for the most relevant documents based on the query.

    Args:
        query (str): The query string to search for.
        top_k (int): The number of top similar documents to return.
    """
    
    query_embedding = generate_embedding(query)
    indexer = build_indexer()
    results = indexer.search(
        query_embedding=query_embedding,
        top_k=top_k
    )
    
    return results

if __name__ == "__main__":
    question = "Why is Bamboo getting Permission denied?"
    results = search_knowledge_base(question, top_k=3)
    print(f"Top {len(results)} results for the query: '{question}'")
    
    for result in results:
        print(f"\nDocument ID: {result['id']}")
        print(f"Score: {result['score']}")
        print(f"Text: {result['text']}")
        print(f"Metadata: {result['metadata']}")