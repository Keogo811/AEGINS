# rag_memory.py — Couche 4 : RAG borné sur le journal intime
# Étape 1 : contrat uniquement. Aucune implémentation.
# Garde-fous figés AVANT toute logique (décision : la psyché d'abord).

# --- Garde-fous (les 5 bornes, non négociables) ---
TOP_K = 3                       # max 3 fragments par retrieval
MAX_WORDS_TOTAL = 150           # max ~150 mots injectés dans le prompt
SIMILARITY_THRESHOLD = 0.5      # sous ce seuil, on n'injecte rien (silence > bruit)
EXCLUDE_RECENT_SESSIONS = 1     # pénalise les chunks retrievés à la session précédente

# Label explicite pour le prompt : l'écho est passé, pas vérité actuelle
ECHO_LABEL = "### Échos du journal — fragments passés, pas vérité actuelle"


def index_journal_file(file_path: str, entity_name: str) -> int:
    """
    Indexe un fichier journal dans ChromaDB.
    Idempotent : ré-indexer ne duplique pas (IDs déterministes).
    Retourne le nombre de chunks indexés.
    """
    raise NotImplementedError


def retrieve(query: str, entity_name: str, top_k: int = TOP_K) -> list[dict]:
    """
    Cherche les fragments de journal les plus proches sémantiquement de `query`.
    Applique : seuil de similarité, cap top_k, exclusion des chunks récents.
    Retourne une liste de dicts : {text, date, source, score}.
    Retourne [] si Ollama/ChromaDB échoue (fail-safe, pas de crash).
    """
    raise NotImplementedError


def format_echoes_for_prompt(echoes: list[dict]) -> str:
    """
    Formate les échos pour injection dans le prompt système.
    Applique le cap MAX_WORDS_TOTAL (tronque si dépassement).
    Retourne "" si echoes est vide (pas de bloc vide dans le prompt).
    """
    raise NotImplementedError