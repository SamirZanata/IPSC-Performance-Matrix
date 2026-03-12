from app.database.vector_store import IPSCVectorStore

def run_ingestion():
    store = IPSCVectorStore()
    store.ingest_pdf("data/2026-Handgun-pt_BRA.pdf")

if __name__ == "__main__":
    run_ingestion()
