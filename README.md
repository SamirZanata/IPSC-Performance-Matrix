# 🎯 IPSC Performance Matrix — AI Microservice for Shooters

[![Build Passing](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker)](https://docker.com)

> **Artificial Intelligence microservice** that combines **official rules**, **ballistic calculations**, and **LLM** for IPSC (International Practical Shooting Confederation) shooters.

---

## 📖 About the Project

**IPSC Performance Matrix** is an AI backend designed for those who train and compete in **practical shooting**. The system answers questions about **Handgun rulebook rules**, computes **Hit Factor** and **Power Factor** according to the sport’s formulas, and guides the user based on the regulation — all via chat, with answers grounded in **RAG** and **Function Calling**.

**Highlights:**

- 🤖 Specialized assistant for IPSC (divisions, equipment, penalties, distances).
- 📐 Accurate **Hit Factor** (points ÷ time) and **Power Factor** (Major/Minor) calculations.
- 📚 Answers anchored in the **official rulebook** (semantic search).
- 🛡️ Guidance to consult a Range Officer (RO) when the information is not in the rulebook.

---

## 🛠 Tech Stack

| Category   | Stack |
|-----------|--------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI / LLM** | Google Gemini 2.5 Flash, Function Calling (Tools) |
| **RAG** | ChromaDB (vector database), local embeddings (DefaultEmbeddingFunction) |
| **PDF** | PyPDF (manual extraction and chunking) |
| **Infra** | Docker, Docker Compose |
| **API docs** | Swagger UI (`/docs`) |

---

## 🏗 Architecture Overview

- **Microservice** in Python with FastAPI and Docker.
- **Brain:** Integration with **Google Gemini 2.5 Flash** using **Function Calling** for Hit Factor and Power Factor calculations.
- **RAG:** Semantic search over the Handgun rulebook with **ChromaDB** and local embeddings (no external embedding API).
- **Infrastructure:** Application and persistent volumes orchestrated with **Docker Compose** (vector store in `./data`).

---

## 🚀 How to Run

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- A `.env` file at the project root with your Gemini API key, for example:
  ```env
  GOOGLE_API_KEY=your_key_here
  ```
  *(or `GEMINI_API_KEY`, as used in the code.)*

### 1. Clone and enter the project

```bash
git clone <repository-url>
cd ipsc-performance-matrix
```

### 2. Start the service with Docker Compose

```bash
docker compose up --build -d
```

The service runs on port **8000**. The vector store lives in `./data` (persistent volume).

### 3. (Optional) Ingest the rulebook into ChromaDB

If the vector store is not populated yet, run the ingestion (e.g. inside the container or on the host with the same `./data`):

```bash
# Example: run inside the container
docker compose exec ai-service python -m ingest_manual
```

Ensure the rulebook PDF (e.g. `data/2026-Handgun-pt_BRA.pdf`) is in the path expected by the script.

### 4. API documentation (Swagger)

Open in your browser:

```
http://localhost:8000/docs
```

---

## 📡 Sample Query (cURL)

Example request to the assistant (rules + calculations):

```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the minimum distance for metal targets according to the rulebook? And calculate the hit factor for 120 points in 18 seconds."}'
```

**Expected response (example):**

```json
{
  "answer": "According to the rulebook, the minimum distance for metal targets is... As for the hit factor: 120 ÷ 18 = 6.67.",
  "status": "success"
}
```

The model automatically chooses between **querying the rulebook (RAG)** and **calculating Hit Factor / Power Factor** via tools.

---

## 🔌 HTTP contract (e.g. Alpha Tracker Pro / Nest)

Use this to align another service (env `AI_SERVICE_URL`, Docker DNS) without guessing.

| Item | Value |
|------|--------|
| **Method** | `POST` |
| **Path** | `/v1/chat` |
| **Header** | `Content-Type: application/json` |
| **Body** | `{ "message": "<user text>" }` only (no `userId` in this API; add that in the caller if you need per-user context server-side). |
| **200 OK** | JSON including **`answer`** (string) with the model reply. This service also returns **`status`**: `"success"`. Clients that accept **`response`** as a fallback can rely on **`answer`** here. |
| **Errors** | HTTP **≥ 400** (e.g. invalid request, server error). Callers may surface these as generic upstream errors. |

**Manual check** (adjust host/port if the engine is not on localhost):

```bash
curl -sS -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Olá"}'
```

Expect a JSON body with a string **`answer`**.

### Docker DNS (`ENOTFOUND` / `EAI_AGAIN` on `ipsc-ai-engine`)

Inside Docker, the hostname **`ipsc-ai-engine`** resolves only for containers attached to the **same user-defined bridge network** as this service. This compose file sets `container_name: ipsc-ai-engine` and attaches the app to **`ipsc-network`**.

- **Default Compose:** the network is often named **`{project_directory}_ipsc-network`** (e.g. `ipsc-performance-matrix_ipsc-network`). From the **host**, use `http://localhost:8000`, not `ipsc-ai-engine`.
- **Shared network with another stack (e.g. Nest):** create a network once (`docker network create ipsc-network`) and in **both** compose files declare that network as **`external: true`** with the same name, attach both services, and set `AI_SERVICE_URL` to `http://ipsc-ai-engine:8000/v1/chat` (or whatever hostname/port/path you standardize on).
- **Caller on the host, engine in Docker:** use `http://127.0.0.1:8000/v1/chat` (published port), not `ipsc-ai-engine`.

---

## 📁 Project Structure (summary)

```
ipsc-performance-matrix/
├── app/
│   ├── api.py              # FastAPI, /v1/chat and /health routes
│   ├── main.py             # Chat test script (Gemini + tools)
│   ├── database/
│   │   └── vector_store.py # ChromaDB, PDF ingestion and consultar_regras_ipsc
│   └── tools/
│       └── ballistics.py   # calculate_hit_factor, check_power_factor
├── data/                   # Rulebook PDF + vector_db (persistent)
├── docker-compose.yml
├── dockerfile
├── ingest_manual.py        # Script to populate ChromaDB
├── requirements.txt
└── .env                    # GOOGLE_API_KEY or GEMINI_API_KEY
```

---

## 🔗 Links

- **LinkedIn:** [Samir Zanata](https://www.linkedin.com/in/samir-zanata-jr-a7a3261b5/)

---

## 📄 License

Portfolio project. See the repository for terms of use.
