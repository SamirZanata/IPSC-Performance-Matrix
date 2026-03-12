import os
import logging
import chromadb
from pypdf import PdfReader
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)

_store_instance = None


def _get_store(db_path=None):
    global _store_instance
    if _store_instance is None:
        _store_instance = IPSCVectorStore(db_path=db_path or "./data/vector_db")
    return _store_instance


class IPSCVectorStore:
    def __init__(self, db_path="./data/vector_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="ipsc_rules_handgun",
            embedding_function=self.ef
        )

    def split_text_with_overlap(self, text, chunk_size=1000, overlap=200):
        """Corta o texto em pedaços garantindo contexto entre eles."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
        return chunks

    def ingest_pdf(self, pdf_path):
        """Lê o PDF, processa e guarda no Banco Vetorial."""
        if not os.path.exists(pdf_path):
            logger.error("Arquivo não encontrado: %s", pdf_path)
            return

        reader = PdfReader(pdf_path)
        all_chunks = []
        all_metadatas = []
        all_ids = []

        logger.info("Processando manual: %s", pdf_path)

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if not page_text:
                continue

            page_chunks = self.split_text_with_overlap(page_text)
            for j, chunk in enumerate(page_chunks):
                all_chunks.append(chunk)
                all_metadatas.append({"page": i + 1, "chunk": j})
                all_ids.append(f"p{i+1}_c{j}")

        self.collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        logger.info("Sucesso: %d fragmentos indexados", len(all_chunks))

    def ask_rules(self, question, n_results=3):
        """Busca os fragmentos mais similares à pergunta."""
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        return results["documents"][0]


def consultar_regras_ipsc(pergunta: str) -> str:
    """
    Consulta o manual oficial de Handgun do IPSC para responder dúvidas sobre regras,
    divisões, equipamentos e penalidades. Use esta função sempre que o usuário
    tiver uma dúvida técnica sobre o esporte.
    """
    logger.info("Tool acionada: consultar_regras_ipsc | pergunta=%s", pergunta[:80])

    store = _get_store()
    resultados = store.ask_rules(pergunta, n_results=3)
    contexto = "\n---\n".join(resultados)
    return contexto
