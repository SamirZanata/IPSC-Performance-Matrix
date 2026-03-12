import os
import chromadb
from pypdf import PdfReader
from chromadb.utils import embedding_functions

class IPSCVectorStore:
    def __init__(self, db_path="./data/vector_db"):
        # Inicializa o cliente persistente (cria a pasta se não existir)
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Modelo de Embedding (Roda localmente, sem custo de API)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Cria ou recupera a coleção (nossa "tabela" de regras)
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
            print(f"Erro: Arquivo {pdf_path} não encontrado.")
            return

        reader = PdfReader(pdf_path)
        all_chunks = []
        all_metadatas = []
        all_ids = []

        print(f"--- Processando manual: {pdf_path} ---")

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if not page_text: continue

            # Dividir a página em pedaços com sobreposição
            page_chunks = self.split_text_with_overlap(page_text)
            
            for j, chunk in enumerate(page_chunks):
                all_chunks.append(chunk)
                all_metadatas.append({"page": i + 1, "chunk": j})
                all_ids.append(f"p{i+1}_c{j}")

        # Inserção em massa (Batch insert) no Chroma
        self.collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        print(f"--- Sucesso: {len(all_chunks)} fragmentos indexados! ---")

    def ask_rules(self, question, n_results=3):
        """Busca os fragmentos mais similares à pergunta."""
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        return results['documents'][0]

# --- ESTA FUNÇÃO FICA FORA DA CLASSE ---
def consultar_regras_ipsc(pergunta: str) -> str:
    """
    Consulta o manual oficial de Handgun do IPSC para responder dúvidas sobre regras, 
    divisões, equipamentos e penalidades. Use esta função sempre que o usuário 
    tiver uma dúvida técnica sobre o esporte.
    """
    print(f"\n[DEBUG] Consultando o manual sobre: {pergunta}")
    
    store = IPSCVectorStore() # Ele vai abrir a pasta data/vector_db existente
    resultados = store.ask_rules(pergunta, n_results=3)
    
    # Unimos os 3 pedaços mais relevantes em um texto só para a IA ler
    contexto = "\n---\n".join(resultados)
    return contexto