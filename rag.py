import os

from dotenv import load_dotenv
from google import genai
from indexer import build_indexer
from rag_prompt import build_rag_prompt
from embedding import generate_embedding
from context_builder import build_context


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=API_KEY)

def generate_answer(question, context):
    """Generate an answer to the question based on the provided context using GenAI."""
    prompt = build_rag_prompt(question, context)
    
    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text
    
    return response.output_text.strip()

def retrive_context(question, store, top_k=3):
    """Retrieve relevant context from the knowledge base based on the question."""
    query_embedding = generate_embedding(question)
    results = store.search(
        query_embedding,
        top_k=top_k
    )
    
    context = build_context(results)
    for result in results:
        print(f"\nChunk ID: {result['id']}")
        print(f"Score: {result['score']:.4f}")
        print(result["text"])
    return context, results
    



def answer_question(question, store):
    """Run retrieval-augmented generation (RAG) to answer a question based on the knowledge base."""
    
    context, results = retrive_context(question, store)
    
    print("\n--- Retrieved chunks for debugging ---")

    for result in results:
        print(f"\nChunk ID: {result['id']}")
        print(f"Similarity score: {result['score']:.4f}")
        print(f"Source: {result['metadata'].get('source', 'Unknown')}")
        print(f"Text:\n{result['text']}")

    print("\n--- Context sent to Gemini ---")
    print(context)
    
    
    if not context.strip():
        return "Insufficient information", results
    
    answer = generate_answer(question, context)
    return answer, results



def main():
    print("Building the knowledge-base index...")
    store = build_indexer()
    print("Index built successfully.")
    print(
        f"Indexed {len(store.documents)} chunks."
    )
    
    print ("Bamboo Log Analyzer is ready to answer your questions.")
    print ("Type 'exit' to quit the program.")
    while True:
        question = input("\nEnter your question: ")
        if question.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        if not question.strip():
            print("Please enter a valid question.")
            continue
        
        try:
            answer, results = answer_question(question, store)
            print("\nAnswer:", answer)
            print("\nTop relevant chunks:")
            for result in results:
                print(
                    
                    f"Chunk: {result['text']}\nSimilarity Score: {result['score']}\n"
                )
            print()
            
        except Exception as e:
            print(f"Request failed: {e}. Please try again.")







if __name__ == "__main__":
    main()