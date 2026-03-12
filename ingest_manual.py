from app.database.vector_store import IPSCVectorStore

def run_ingestion():
    store = IPSCVectorStore()
    # Ajusta o nome do arquivo para o que está na tua pasta data/
    store.ingest_pdf("data/2026-Handgun-pt_BRA.pdf") 

if __name__ == "__main__":
    run_ingestion()