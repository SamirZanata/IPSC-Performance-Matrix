import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
# Importamos suas funções reais
from tools.ballistics import calculate_hit_factor, check_power_factor

load_dotenv()

# 1. Instanciamos o cliente moderno
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. O segredo: passamos as funções como uma lista para o modelo.
# O SDK vai ler o nome e os parâmetros delas automaticamente.
tools_list = [calculate_hit_factor, check_power_factor]

# 3. Criamos o chat com "Automatic Function Calling" habilitado
chat = client.chats.create(
    model="gemini-2.5-flash", 
    config=types.GenerateContentConfig(
        tools=tools_list,
        temperature=0.1 # Mantemos baixo para evitar "criatividade" em cálculos
    )
)

try:
    # Desafio para a IA: Ela precisa decidir qual função usar.
    pergunta = "Fiz 125 pontos em 14.2 segundos. Qual foi meu Hit Factor?"
    print(f"\nUsuário: {pergunta}")
    
    response = chat.send_message(pergunta)
    
    print(f"\nResposta Final do Agente: {response.text}")

except Exception as e:
    print(f"\n[ERRO]: {e}")