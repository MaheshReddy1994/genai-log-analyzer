
from indexer import build_indexer
from embedding import generate_embedding


# Questions with their expected relevant chunk IDs.
TEST_CASES = [
    {
        "question": "Why is Bamboo getting Permission denied?",
        "expected_chunk_id": "bamboo_chunk_1",
    },
    {
        "question": "Why can't Bamboo connect to the deployment server?",
        "expected_chunk_id": "bamboo_chunk_2",
    },
    {
        "question": "Why can't Bamboo find my deployment script?",
        "expected_chunk_id": "bamboo_chunk_3",
    },
    {
    "question": "The deployment job says permission denied. What should I check?",
    "expected_chunk_id": "bamboo_chunk_1",
},
{
    "question": "Bamboo cannot reach the target deployment machine. How can I troubleshoot it?",
    "expected_chunk_id": "bamboo_chunk_2",
},
{
    "question": "The script path configured in my Bamboo job seems wrong. What should I verify?",
    "expected_chunk_id": "bamboo_chunk_3",
}
]

TOP_K = 3


def evaluate_retrieval():
    # Build the knowledge-base index once.
    store = build_indexer()

    hits = 0
    total_tests = len(TEST_CASES)

    for test in TEST_CASES:
        question = test["question"]
        expected_id = test["expected_chunk_id"]

        # Convert the user's question into an embedding.
        query_embedding = generate_embedding(question)

        # Retrieve the top-K most similar chunks.
        results = store.search(
            query_embedding,
            top_k=TOP_K
        )

        # Extract the IDs returned by the vector store.
        retrieved_ids = [result["id"] for result in results]

        # Check whether the expected chunk was retrieved.
        hit = expected_id in retrieved_ids

        if hit:
            hits += 1

        print("\n" + "=" * 60)
        print(f"Question: {question}")
        print(f"Expected chunk: {expected_id}")
        print(f"Retrieved chunks: {retrieved_ids}")
        print(f"Hit@{TOP_K}: {hit}")

    # Calculate the overall retrieval hit rate.
    hit_rate = hits / total_tests if total_tests else 0

    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Successful retrievals: {hits}")
    print(f"Failed retrievals: {total_tests - hits}")
    print(f"Hit Rate@{TOP_K}: {hit_rate:.2%}")


if __name__ == "__main__":
    evaluate_retrieval()
