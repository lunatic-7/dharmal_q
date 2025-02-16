import os
import faiss
import numpy as np
from openai import OpenAI
import pickle
from dotenv import load_dotenv
from typing import List

load_dotenv()
client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SCRIPT_FILE = "harry_potter.txt"
INDEX_FILE = "faiss_index.pkl"
CHUNKS_FILE = "chunks.pkl"

def split_script_into_chunks(file_path: str, chunk_size=300) -> List[str]:
    """Splits script into fixed-size text chunks (e.g., 300 words each)."""
    with open(file_path, "r", encoding="utf-8") as file:
        words = file.read().split()  # Split by words
    
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def get_embedding(text: str) -> List[float]:
    """Gets the embedding for a given text using OpenAI API."""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    return response.data[0].embedding

def build_faiss_index(script_path: str):
    """Builds and saves a FAISS index using chunked embeddings."""
    chunks = split_script_into_chunks(script_path, chunk_size=300)

    if not chunks:
        print("❌ No text chunks found! Check script file.")
        return

    # Generate embeddings for each chunk
    embeddings = np.array([get_embedding(chunk) for chunk in chunks], dtype="float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save FAISS index
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)

    # Save chunks for later retrieval
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Indexed {len(chunks)} text chunks and saved FAISS index.")

if __name__ == "__main__":
    build_faiss_index(SCRIPT_FILE)
