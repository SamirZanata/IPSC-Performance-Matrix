FROM python:3.11-slim

# Dependências de sistema para o ChromaDB e PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variável de ambiente para garantir que o log apareça no console do Docker
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]