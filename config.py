# ============================================================
# Configuration générale du projet AEGINS
# ============================================================

# Nom de l'entité active. Détermine où vivent ses données.
# "alice"      -> data/alice/       + identites/alice.md
# "alice_zero" -> data/alice_zero/  + identites/alice_zero.md
# "elise"      -> data/elise/       + identites/elise.md
ENTITE = "alice"


# ============================================================
# Backend LLM (PARTAGÉ par toutes les entités)
# ============================================================
#
#   "ollama"  -> modèle local, abliterated, lent mais libre
#   "groq"    -> API distante, rapide mais censurée
#
# Peut être surchargé à chaud via data/backend.txt
#
LLM_BACKEND = "ollama"

OLLAMA_MODELE_PRINCIPAL = "huihui_ai/qwen3-abliterated:8b"
OLLAMA_MODELE_RAPIDE = "huihui_ai/qwen3-abliterated:4b"

GROQ_MODELE_PRINCIPAL = "qwen/qwen3.8-27b"
GROQ_MODELE_RAPIDE = "llama-3.1-8b-instant"