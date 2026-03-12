# 🎯 IPSC Performance Matrix — Microserviço de IA para Atiradores

[![Build Passing](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker)](https://docker.com)

> **Microserviço de Inteligência Artificial** que une **regras oficiais**, **cálculos balísticos** e **LLM** para atiradores de IPSC (International Practical Shooting Confederation).

---

## 📖 Sobre o Projeto

O **IPSC Performance Matrix** é um backend de IA pensado para quem treina e compete em **tiro prático**. O sistema responde dúvidas sobre **regras do manual oficial de Handgun**, calcula **Hit Factor** e **Power Factor** conforme as fórmulas do esporte e orienta o usuário com base no regulamento — tudo via chat, com respostas fundamentadas em **RAG** e **Function Calling**.

**Destaques:**

- 🤖 Assistente especializado em IPSC (divisões, equipamentos, penalidades, distâncias).
- 📐 Cálculos precisos de **Hit Factor** (pontos ÷ tempo) e **Power Factor** (Major/Minor).
- 📚 Respostas ancoradas no **manual oficial** em português (busca semântica).
- 🛡️ Orientação para consultar um Range Officer (RO) quando a informação não estiver no manual.

---

## 🛠 Tecnologias

| Categoria        | Stack |
|------------------|--------|
| **Backend**      | Python 3.11, FastAPI, Uvicorn |
| **IA / LLM**     | Google Gemini 2.5 Flash, Function Calling (Tools) |
| **RAG**          | ChromaDB (vector database), embeddings locais (DefaultEmbeddingFunction) |
| **PDF**          | PyPDF (extração e chunking do manual) |
| **Infra**        | Docker, Docker Compose |
| **Doc da API**   | Swagger UI (`/docs`) |

---

## 🏗 Arquitetura em Resumo

- **Microserviço** em Python com FastAPI e Docker.
- **Cérebro:** Integração com **Google Gemini 2.5 Flash** usando **Function Calling** para cálculos de Hit Factor e Power Factor.
- **RAG:** Busca semântica no manual de Handgun com **ChromaDB** e embeddings locais (sem API de embedding externa).
- **Infraestrutura:** Aplicação e volumes persistentes orquestrados com **Docker Compose** (banco vetorial em `./data`).

---

## 🚀 Como Rodar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
- Arquivo `.env` na raiz do projeto com sua chave do Gemini, por exemplo:
  ```env
  GOOGLE_API_KEY=sua_chave_aqui
  ```
  *(ou `GEMINI_API_KEY`, conforme usado no código.)*

### 1. Clonar e entrar no projeto

```bash
git clone <url-do-repositorio>
cd ipsc-performance-matrix
```

### 2. Subir o serviço com Docker Compose

```bash
docker compose up --build -d
```

O serviço sobe na porta **8000**. O banco vetorial fica em `./data` (volume persistente).

### 3. (Opcional) Ingerir o manual no ChromaDB

Se ainda não tiver o banco vetorial populado, rode a ingestão (por exemplo, dentro do container ou no host com o mesmo `./data`):

```bash
# Exemplo: executar dentro do container
docker compose exec ai-service python -m ingest_manual
```

Certifique-se de que o PDF do manual (ex.: `data/2026-Handgun-pt_BRA.pdf`) está no lugar esperado pelo script.

### 4. Documentação da API (Swagger)

Acesse no navegador:

```
http://localhost:8000/docs
```

---

## 📡 Demonstração de Query (cURL)

Exemplo de pergunta ao assistente (regras + cálculos):

```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual a distância mínima para alvos metálicos segundo o manual? E calcula o hit factor para 120 pontos em 18 segundos."}'
```

**Resposta esperada (exemplo):**

```json
{
  "answer": "Segundo o manual, a distância mínima para alvos metálicos é... Quanto ao hit factor: 120 ÷ 18 = 6,67.",
  "status": "success"
}
```

O modelo escolhe automaticamente entre **consultar o manual (RAG)** e **calcular Hit Factor / Power Factor** via ferramentas.

---

## 📁 Estrutura do Projeto (resumida)

```
ipsc-performance-matrix/
├── app/
│   ├── api.py              # FastAPI, rota /v1/chat e /health
│   ├── main.py             # Script de teste do chat (Gemini + tools)
│   ├── database/
│   │   └── vector_store.py # ChromaDB, ingestão do PDF e consultar_regras_ipsc
│   └── tools/
│       └── ballistics.py   # calculate_hit_factor, check_power_factor
├── data/                   # PDF do manual + vector_db (persistente)
├── docker-compose.yml
├── dockerfile
├── ingest_manual.py        # Script para popular o ChromaDB
├── requirements.txt
└── .env                    # GOOGLE_API_KEY ou GEMINI_API_KEY
```

---

## 🔗 Links

- **LinkedIn:** [Seu perfil aqui](https://www.linkedin.com/in/samir-zanata-jr-a7a3261b5/)

---

## 📄 Licença

Projeto de portfólio. Consulte o repositório para termos de uso.
