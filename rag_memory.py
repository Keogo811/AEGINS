# rag_memory.py — Couche 4 : RAG borné sur le journal intime
# Arc 13.2 : Implémentation de l'indexation.

import os
import chromadb
import ollama

# --- Garde-fous ---
TOP_K = 3
MAX_WORDS_TOTAL = 150
SIMILARITY_THRESHOLD = 0.5
EXCLUDE_RECENT_SESSIONS = 1
ECHO_LABEL = "### Échos du journal — fragments passés, pas vérité actuelle"

# On place la DB dans data/ pour ne pas encombrer la racine
CHROMA_PATH = "./data/chroma_db"
EMBED_MODEL = "nomic-embed-text"


def get_collection(entity_name: str):
    """Récupère ou crée la collection pour une entité."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=f"journal_{entity_name}")


def embed(text: str) -> list[float]:
    """Embedding via Ollama local."""
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def chunk_text(text: str) -> list[str]:
    """Découpe par paragraphe (double newline). Simple et inspectable."""
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def index_journal_file(file_path: str, entity_name: str) -> int:
    """
    Indexe un fichier journal dans ChromaDB.
    Idempotent : ré-indexer ne duplique pas (IDs déterministes).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return 0

    chunks = chunk_text(text)
    if not chunks:
        return 0

    collection = get_collection(entity_name)
    # ID déterministe basé sur le nom du fichier et l'index du chunk
    base_id = f"{entity_name}::{os.path.basename(file_path)}"

    ids = [f"{base_id}::{i}" for i in range(len(chunks))]
    
    print(f"Vectorisation de {len(chunks)} chunk(s) en cours...")
    embeddings = [embed(c) for c in chunks]
    
    metadatas = [
        {"source": file_path, "entity": entity_name, "chunk": i}
        for i in range(len(chunks))
    ]

    # upsert = idempotent (add planterait si l'ID existe déjà)
    collection.upsert(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )
    return len(chunks)


# --- Les signatures suivantes restent vides pour l'instant ---
def retrieve(query: str, entity_name: str, top_k: int = TOP_K) -> list[dict]:
    raise NotImplementedError

def format_echoes_for_prompt(echoes: list[dict]) -> str:
    raise NotImplementedError