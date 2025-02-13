import os
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

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# Store chat history (In-memory dictionary)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

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

# Create a new session
@app.get("/new_session")
async def new_session():
    session_id = str(uuid4())  # Generate a unique session ID
    chat_sessions[session_id] = []  # Initialize empty history
    return {"session_id": session_id}

# Chat with history
@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    character = request.character
    user_message = request.user_message

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OpenAI API Key")

    if session_id not in chat_sessions:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    # Retrieve character's personality
    character_prompt = CHARACTER_PROMPTS.get(character, f"You are {character}, reply in their style.")

    # Store user message in history
    chat_sessions[session_id].append({"sender": "User", "text": user_message})

    # Format chat history for LLM context
    history = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in chat_sessions[session_id]])
    
    messages = [
        SystemMessage(content=character_prompt),
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
