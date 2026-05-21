from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "OK - OrthoAI online"}

@app.post("/analisar")
async def analisar(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system="Você é um especialista sênior em ortodontia com foco em alinhadores termoformados. Responda sempre em português brasileiro. Seja preciso, técnico e clinicamente fundamentado.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"resultado": message.content[0].text}

