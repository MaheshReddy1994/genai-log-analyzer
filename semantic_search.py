import math
from embedding import generate_embedding

def cosine_similarity(vector_a, vector_b):
    """Calculate the cosine similarity between two vectors.

    Args:
        vector_a (_type_): _description_
        vector_b (_type_): _description_

    Returns:
        float: The cosine similarity between the two vectors.
    """
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )
    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )
    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

def search_chunks(chunks, query, top_k=2):
    """
    Searches for the most similar chunks to the given query based on cosine similarity.

    Args:
        chunks (list): A list of text chunks.
        query (str): The query string to compare against the chunks.
        top_k (int): The number of top similar chunks to return.
        """
    query_embedding = generate_embedding(query)
    results = []
    for chunk in chunks:
        chunk_embedding = generate_embedding(chunk)
        similarity_score = cosine_similarity(query_embedding, chunk_embedding)
        results.append({
            "chunk": chunk,
            "similarity_score": similarity_score
        })
        
    results.sort(
        key = lambda item: item["similarity_score"],
        reverse = True
    )
    
    return results[:top_k]


if __name__ == "__main__":

    chunks = [
        "Bamboo deployment failed because the service account does not have execute permission.",
        "Bamboo cannot connect to the deployment server. Check network connectivity and firewall rules.",
        "The deployment script was not found at the configured path."
    ]

    query = "Why am I getting permission denied when Bamboo runs my script?"

    results = search_chunks(
        chunks,
        query,
        top_k=2
    )

    for result in results:
        print("\nSimilarity:", result["similarity_score"])
        print("Chunk:", result["chunk"])

    