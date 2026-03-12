import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.tools.ballistics import calculate_hit_factor, check_power_factor
from app.database.vector_store import consultar_regras_ipsc

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

tools_list = [calculate_hit_factor, check_power_factor, consultar_regras_ipsc]

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        tools=tools_list,
        temperature=0.1
    )
)

try:
    pergunta = "Qual a distância mínima para alvos metálicos segundo o manual?"
    print(f"\nUsuário: {pergunta}")

    response = chat.send_message(pergunta)

    print(f"\nResposta Final do Agente: {response.text}")

except Exception as e:
    print(f"\n[ERRO]: {e}")
