import os
import config

CHEMIN_BACKEND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", "backend.txt"
)


def backend_actuel():
    """Retourne 'ollama' ou 'groq'. Priorité au fichier data/backend.txt,
    sinon valeur par défaut dans config.py."""
    if os.path.exists(CHEMIN_BACKEND):
        with open(CHEMIN_BACKEND, "r", encoding="utf-8") as f:
            valeur = f.read().strip().lower()
        if valeur in ("ollama", "groq"):
            return valeur
    return config.LLM_BACKEND


def definir_backend(nom):
    """Change le backend actif et le persiste dans data/backend.txt."""
    nom = nom.strip().lower()
    if nom not in ("ollama", "groq"):
        raise ValueError("backend doit être 'ollama' ou 'groq'")
    os.makedirs(os.path.dirname(CHEMIN_BACKEND), exist_ok=True)
    with open(CHEMIN_BACKEND, "w", encoding="utf-8") as f:
        f.write(nom)
    return nom


def appeler_llm(messages, modele_principal=True):
    """Envoie les messages au backend actif.
    Retourne un tuple (contenu, pensee).
    - Ollama : pensee peut être remplie (thinking).
    - Groq   : pensee est toujours vide (pas de thinking exposé)."""
    backend = backend_actuel()
    if backend == "ollama":
        return _appeler_ollama(messages, modele_principal)
    else:
        return _appeler_groq(messages, modele_principal)


def _appeler_ollama(messages, modele_principal):
    import ollama
    modele = config.OLLAMA_MODELE_PRINCIPAL if modele_principal else config.OLLAMA_MODELE_RAPIDE
    reponse = ollama.chat(model=modele, messages=messages, think=True)
    contenu = reponse["message"].get("content", "")
    pensee = reponse["message"].get("thinking", "")
    return contenu, pensee


def _appeler_groq(messages, modele_principal):
    from groq import Groq
    from groq_key import GROQ_API_KEY
    modele = config.GROQ_MODELE_PRINCIPAL if modele_principal else config.GROQ_MODELE_RAPIDE
    client = Groq(api_key=GROQ_API_KEY)
    reponse = client.chat.completions.create(model=modele, messages=messages)
    contenu = reponse.choices[0].message.content or ""
    return contenu, ""

def appeler_llm_force(messages, modele_principal=True, backend=None):
    """Comme appeler_llm, mais force un backend précis,
    indépendamment du backend actif."""
    if backend == "ollama":
        return _appeler_ollama(messages, modele_principal)
    elif backend == "groq":
        return _appeler_groq(messages, modele_principal)
    else:
        return appeler_llm(messages, modele_principal)