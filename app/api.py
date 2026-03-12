import sys
import os
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

from app.tools.ballistics import calculate_hit_factor, check_power_factor
from app.database.vector_store import consultar_regras_ipsc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _get_api_key():
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key or not key.strip():
        raise ValueError(
            "API key not found. Set GOOGLE_API_KEY or GEMINI_API_KEY in .env or environment."
        )
    return key.strip()


def _get_model():
    if _get_model._instance is None:
        _get_model._instance = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            tools=[calculate_hit_factor, check_power_factor, consultar_regras_ipsc],
            system_instruction=(
                "Você é um assistente especializado em IPSC (International Practical Shooting Confederation). "
                "Use as ferramentas de cálculo para performance e a consulta ao manual para regras. "
                "Seja preciso e, se não encontrar a informação no manual, oriente o usuário a consultar um Range Officer (RO)."
            ),
        )
    return _get_model._instance


_get_model._instance = None

app = FastAPI(title="IPSC Intelligence Service")

try:
    genai.configure(api_key=_get_api_key())
    _get_model()
    logger.info("IPSC Intelligence Service started; Gemini model singleton initialized")
except ValueError as e:
    logger.critical("Startup failed: %s", e)
    raise SystemExit(1) from e


class ChatRequest(BaseModel):
    message: str


@app.post("/v1/chat")
async def chat(request: ChatRequest):
    try:
        model = _get_model()
        chat_session = model.start_chat(enable_automatic_function_calling=True)
        response = chat_session.send_message(request.message)
        return {
            "answer": response.text,
            "status": "success",
        }
    except ValueError as e:
        logger.warning("Validation error: %s", e)
        raise HTTPException(status_code=400, detail="Requisição inválida. Verifique os dados enviados.") from e
    except Exception as e:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar sua mensagem. Tente novamente ou consulte o suporte.",
        ) from e


@app.get("/health")
async def health():
    return {"status": "alive", "service": "ipsc-ai-engine"}
