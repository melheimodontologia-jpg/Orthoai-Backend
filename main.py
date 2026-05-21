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
    try:
        body = await request.json()
        prompt = body.get("prompt", "")

        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not api_key:
            return {"erro": "API KEY não encontrada no servidor"}

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # modelo mais estável
            max_tokens=2000,
            system="Você é um especialista sênior em ortodontia com foco em alinhadores termoformados. Responda sempre em português brasileiro.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        resposta = ""
        if message.content:
            for item in message.content:
                if item.type == "text":
                    resposta += item.text

        return {"resultado": resposta}

    except Exception as e:
        return {"erro": str(e)}

