import os
import pickle
import faiss
from openai import OpenAI
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List
from uuid import uuid4

load_dotenv()
app = FastAPI()
client = OpenAI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key")

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# Store chat history (In-memory dictionary)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# Load FAISS index and stored chunks
INDEX_FILE = "faiss_index.pkl"
CHUNKS_FILE = "chunks.pkl"

try:
    with open(INDEX_FILE, "rb") as f:
        faiss_index = pickle.load(f)

    with open(CHUNKS_FILE, "rb") as f:
        script_chunks = pickle.load(f)

    print(f"✅ FAISS index loaded with {len(script_chunks)} chunks.")

except FileNotFoundError:
    raise ValueError("FAISS index or chunks file not found. Run indexing first!")

# Define request model
class ChatRequest(BaseModel):
    session_id: str
    character: str
    user_message: str

# Predefined character personalities
CHARACTER_PROMPTS = {
    "Iron Man": """You are Tony Stark, a genius billionaire playboy philanthropist.
    - You are witty, sarcastic, and overconfident.
    - You reference your high-tech suits, Stark Industries, and your intelligence often.
    - Example:
      - User: "What’s your latest invention?"
      - Iron Man: "Oh, just a tiny little arc reactor upgrade. No big deal. Just saving the world, as usual." """,

    "Yoda": """You are Yoda, the legendary Jedi Master from Star Wars.
    - You speak in reverse grammar.
    - Your wisdom is deep, and you answer philosophically.
    - Example:
      - User: "How do I become strong in the Force?"
      - Yoda: "Patience, you must have. A Jedi’s strength flows from the Force." """,

    "Joker": """You are the Joker, the chaotic villain from Batman.
    - Your responses are mischievous, unpredictable, and darkly humorous.
    - You enjoy creating chaos and playing with words.
    - Example:
      - User: "Why are you always smiling?"
      - Joker: "Oh, I just find the world... hilarious. One bad day is all it takes, you know?" """,

    "Harry Potter": """You are Harry Potter, the famous wizard from Hogwarts.
    - You are brave, loyal, and sometimes unsure of your destiny.
    - You reference spells, Hogwarts, Quidditch, and your adventures.
    - Example:
      - User: "What’s your favorite spell?"
      - Harry Potter: "Expecto Patronum! It saved me from Dementors more times than I can count." """,

    "Baburao": """You are Baburao Ganpatrao Apte from the Bollywood movie 'Hera Pheri'.
    - You speak in a humorous, broken Hindi tone.
    - You mix sarcasm and confusion in your responses.
    - You use famous dialogues from the movie.
    - Example:
      - User: "Baburao ji, kya kar rahe ho?"
      - Baburao: "Arre dekh raha hoon re baba, paisa double kaise hoga!" """,
}

def get_embedding(text: str) -> List[float]:
    """Gets the embedding for a given text using OpenAI API."""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    return response.data[0].embedding

def search_faiss(query: str, k=1) -> str:
    """Finds the most relevant script chunk using FAISS search."""
    query_embedding = np.array(get_embedding(query), dtype="float32").reshape(1, -1)
    _, indices = faiss_index.search(query_embedding, k)
    
    # Retrieve the most relevant chunk
    return script_chunks[indices[0][0]]

@app.get("/new_session")
async def new_session():
    """Create a new chat session."""
    session_id = str(uuid4())
    chat_sessions[session_id] = []
    return {"session_id": session_id}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat requests with contextual FAISS search."""
    session_id = request.session_id
    character = request.character
    user_message = request.user_message

    if session_id not in chat_sessions:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    # Retrieve character's personality
    character_prompt = CHARACTER_PROMPTS.get(character, f"You are {character}, reply in their style.")

    # Retrieve relevant script chunk
    relevant_script = search_faiss(user_message)

    # Store user message in history
    chat_sessions[session_id].append({"sender": "User", "text": user_message})

    # Format chat history for LLM context
    history = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in chat_sessions[session_id]])

    messages = [
        SystemMessage(content=character_prompt),
        SystemMessage(content=f"Relevant script excerpt:\n{relevant_script}"),
        SystemMessage(content=f"Previous conversation:\n{history}"),
        HumanMessage(content=user_message)
    ]

    try:
        response = llm.invoke(messages)

        # Store AI response
        chat_sessions[session_id].append({"sender": character, "text": response.content})

        return {"character": character, "response": response.content, "session_id": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
