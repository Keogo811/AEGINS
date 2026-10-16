# ============================================================
# Configuration générale du projet AEGINS
# ============================================================

# Nom de l'entité active. Détermine où vivent ses données.
# "alice"      -> data/alice/       + identites/alice.md
# "alice_zero" -> data/alice_zero/  + identites/alice_zero.md
# "elise"      -> data/elise/       + identites/elise.md
import os as _os

_CHEMIN_ENTITE = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)),
    "data", "entite.txt"
)

def _lire_entite():
    if _os.path.exists(_CHEMIN_ENTITE):
        with open(_CHEMIN_ENTITE, "r", encoding="utf-8") as f:
            nom = f.read().strip()
        if nom:
            return nom
    return "alice"

ENTITE = _lire_entite()


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

# Nombre de souvenirs injectés dans le contexte, selon le backend
OLLAMA_NB_SOUVENIRS = 15
GROQ_NB_SOUVENIRS = 35

OLLAMA_MODELE_PRINCIPAL = "huihui_ai/qwen3-abliterated:8b"
OLLAMA_MODELE_RAPIDE = "huihui_ai/qwen3-abliterated:4b"

GROQ_MODELE_PRINCIPAL = "qwen/qwen3.8-27b"
GROQ_MODELE_RAPIDE = "openai/gpt-oss-20b"