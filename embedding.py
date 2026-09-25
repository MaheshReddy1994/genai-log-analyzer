import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your .env file.")


EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_embedding(text):
    """
    Generates an embedding for the given text using the specified embedding model.
    
    Args:
        text (str): The input text for which to generate the embedding.
        """
    result = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents = text
    )
    
    print (f"Embedding results: {result}")
    
    return result.embeddings[0].values

if __name__ == "__main__":
    text = "Bamboo service account does not have permission."
    embedding = generate_embedding(text)
    
    print("Embedding generated successfully")
    print("Vector dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])
    