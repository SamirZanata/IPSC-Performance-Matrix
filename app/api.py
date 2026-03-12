import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

from app.tools.ballistics import calculate_hit_factor, check_power_factor
from app.database.vector_store import consultar_regras_ipsc

load_dotenv()

app = FastAPI(title="IPSC Intelligence Service")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[calculate_hit_factor, check_power_factor, consultar_regras_ipsc],
    system_instruction=(
        "Você é um assistente especializado em IPSC (International Practical Shooting Confederation). "
        "Use as ferramentas de cálculo para performance e a consulta ao manual para regras. "
        "Seja preciso e, se não encontrar a informação no manual, oriente o usuário a consultar um Range Officer (RO)."
    )
)

class ChatRequest(BaseModel):
    message: str

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    try:
        chat_session = model.start_chat(enable_automatic_function_calling=True)
        response = chat_session.send_message(request.message)

        return {
            "answer": response.text,
            "status": "success"
        }
    except Exception as e:
        print(f"[ERRO] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "alive", "service": "ipsc-ai-engine"}
