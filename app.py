import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

app = FastAPI()
@app.get("/")
def home():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str

@app.post("/chat")
def chat(data: UserInput):

    user_message = data.message.lower()

    emergency_words = [
        "chest pain",
        "difficulty breathing",
        "stroke",
        "heart attack",
        "severe bleeding"
    ]

    for word in emergency_words:
        if word in user_message:
            return {
                "response":
                "⚠️ This may be a medical emergency. Please contact a doctor immediately."
            }

    if client is None:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured.",
        )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": """
You are a helpful AI medical assistant.

Give short and clear answers.

Use simple language.

Keep responses under 6 lines.

Suggest doctor consultation if symptoms are serious.
"""
            },

            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    ai_response = completion.choices[0].message.content

    return {
        "response": ai_response
    }