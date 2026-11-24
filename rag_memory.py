# rag_memory.py — Couche 4 : RAG borné sur le journal intime
# Arc 13.4 : Anti-cristallisation (mémoire de retrieval).

import os
import json
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
    base_id = f"{entity_name}::{os.path.basename(file_path)}"
    ids = [f"{base_id}::{i}" for i in range(len(chunks))]
    
    print(f"Vectorisation de {len(chunks)} chunk(s) en cours...")
    embeddings = [embed(c) for c in chunks]
    
    metadatas = [
        {"source": file_path, "entity": entity_name, "chunk": i}
        for i in range(len(chunks))
    ]

    collection.upsert(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )
    return len(chunks)


def _get_last_echoes_path(entity_name: str) -> str:
    """Retourne le chemin du fichier de mémoire des derniers échos."""
    # On suppose que le dossier de l'entité existe (ex: data/alice/)
    return f"./data/{entity_name}/last_echoes.json"

def _load_last_echo_ids(entity_name: str) -> list[str]:
    """Charge les IDs des échos de la session précédente."""
    path = _get_last_echoes_path(entity_name)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("excluded_ids", [])
    except Exception:
        return []

def _save_last_echo_ids(entity_name: str, ids: list[str]):
    """Sauvegarde les IDs des échos actuels pour la prochaine session."""
    path = _get_last_echoes_path(entity_name)
    # Sécurité : on s'assure que le dossier existe
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"excluded_ids": ids}, f, indent=2)


def retrieve(query: str, entity_name: str, top_k: int = TOP_K) -> list[dict]:
    """
    Cherche les fragments de journal.
    Applique : seuil, top_k, et exclusion des échos de la session précédente.
    Fail-safe : retourne [] en cas d'erreur.
    """
    try:
        collection = get_collection(entity_name)
        if collection.count() == 0:
            return []

        # 1. Charger les IDs à exclure (anti-cristallisation)
        excluded_ids = _load_last_echo_ids(entity_name) if EXCLUDE_RECENT_SESSIONS else []

        query_embedding = embed(query)

        # 2. Préparer la requête (avec ou sans filtre d'exclusion)
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
        
        if excluded_ids:
            # ChromaDB syntax pour "ID n'est pas dans cette liste"
            query_kwargs["where"] = {"id": {"$nin": excluded_ids}}

        results = collection.query(**query_kwargs)

        echoes = []
        current_session_ids = []

        if not results["documents"] or not results["documents"][0]:
            return []

        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            similarity = 1.0 - distance

            if similarity >= SIMILARITY_THRESHOLD:
                echoes.append({
                    "id": results["ids"][0][i], # On garde l'ID pour l'exclusion future
                    "text": results["documents"][0][i],
                    "source": results["metadatas"][0][i]["source"],
                    "score": round(similarity, 3)
                })
                current_session_ids.append(results["ids"][0][i])

        # 3. Sauvegarder les IDs pour la prochaine fois
        if EXCLUDE_RECENT_SESSIONS:
            _save_last_echo_ids(entity_name, current_session_ids)

        # On retire l'ID du retour final pour garder le format propre (optionnel, mais propre)
        for e in echoes:
            del e["id"]

        return echoes

    except Exception as e:
        print(f"[RAG Fail-safe] Erreur lors du retrieve : {e}")
        return []


def format_echoes_for_prompt(echoes: list[dict]) -> str:
    """Signature vide pour l'instant (Arc 13.5)."""
    raise NotImplementedError