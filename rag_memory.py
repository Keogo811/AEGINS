# rag_memory.py — Couche 4 : RAG borné sur le journal intime
# Arc 13.5 : Formatage pour le prompt (label + limite de mots).

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

CHROMA_PATH = "./data/chroma_db"
EMBED_MODEL = "nomic-embed-text"


def get_collection(entity_name: str):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=f"journal_{entity_name}")


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def chunk_text(text: str) -> list[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def index_journal_file(file_path: str, entity_name: str) -> int:
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
    return f"./data/{entity_name}/last_echoes.json"

def _load_last_echo_ids(entity_name: str) -> list[str]:
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
    path = _get_last_echoes_path(entity_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"excluded_ids": ids}, f, indent=2)


def retrieve(query: str, entity_name: str, top_k: int = TOP_K) -> list[dict]:
    try:
        collection = get_collection(entity_name)
        if collection.count() == 0:
            return []

        excluded_ids = _load_last_echo_ids(entity_name) if EXCLUDE_RECENT_SESSIONS else []
        query_embedding = embed(query)

        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
        
        if excluded_ids:
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
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "source": results["metadatas"][0][i]["source"],
                    "score": round(similarity, 3)
                })
                current_session_ids.append(results["ids"][0][i])

        if EXCLUDE_RECENT_SESSIONS:
            _save_last_echo_ids(entity_name, current_session_ids)

        for e in echoes:
            del e["id"]

        return echoes
    except Exception as e:
        print(f"[RAG Fail-safe] Erreur lors du retrieve : {e}")
        return []


def format_echoes_for_prompt(echoes: list[dict]) -> str:
    """
    Formate les échos pour injection dans le prompt système.
    Applique le cap MAX_WORDS_TOTAL.
    Retourne "" si echoes est vide.
    """
    if not echoes:
        return ""

    lines = [ECHO_LABEL + "\n"]
    word_count = 0

    for e in echoes:
        words = e["text"].split()
        
        # Si l'ajout de ce chunk dépasse la limite, on s'arrête là.
        # Simplicité et fiabilité : on préfère couper net plutôt que tronquer un mot au milieu.
        if word_count + len(words) > MAX_WORDS_TOTAL:
            break
            
        lines.append(f"- [{os.path.basename(e['source'])}] {e['text']}\n")
        word_count += len(words)

    # Si même le premier écho était trop long (ou aucun n'a été ajouté), on renvoie vide
    if len(lines) == 1:
        return ""

    return "".join(lines)