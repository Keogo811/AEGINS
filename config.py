# ============================================================
# Configuration du backend LLM
# ============================================================
#
# Change la valeur ci-dessous pour basculer entre les deux :
#
#   "ollama"  -> modèle local, abliterated, lent mais libre
#   "groq"    -> API distante, rapide mais censurée
#
# Le reste d'Alice (mémoire, journal, identité) est identique
# dans les deux cas.
# ============================================================

LLM_BACKEND = "ollama"


# ------------------------------------------------------------
# Paramètres Ollama (local)
# ------------------------------------------------------------
OLLAMA_MODELE_PRINCIPAL = "huihui_ai/qwen3-abliterated:8b"
OLLAMA_MODELE_RAPIDE = "huihui_ai/qwen3-abliterated:4b"


# ------------------------------------------------------------
# Paramètres Groq (API distante)
# ------------------------------------------------------------
# Modèle principal : puissant, pour les réponses d'Alice
GROQ_MODELE_PRINCIPAL = "qwen/qwen3.8-27b"

# Modèle rapide : léger, pour l'évaluation d'importance
GROQ_MODELE_RAPIDE = "llama-3.1-8b-instant"