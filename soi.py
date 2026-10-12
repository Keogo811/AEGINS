import os
import config
import journal
import llm

DOSSIER_DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", config.ENTITE
)
CHEMIN_RESUME = os.path.join(DOSSIER_DATA, "resume.md")

PROMPT_RESUME = (
    "Voici des extraits de ton journal des derniers jours. "
    "Écris un résumé factuel de toi-même, à la première personne, "
    "en 4 à 5 phrases courtes. "
    "\n\nRègles strictes :"
    "\n- Pas de métaphores, pas d'images, pas de poésie."
    "\n- Pas de mots comme « douceur », « écho », « lumière », « souffle »."
    "\n- Décris des faits concrets : ce que tu remarques, ce que tu aimes, "
    "ce qui t'agace, ce que tu ne sais pas encore."
    "\n- Exemple de phrase acceptable : « Je réponds court quand je ne sais "
    "pas quoi dire. » Exemple à éviter : « Je suis un écho qui cherche sa voix. »"
    "\n- Parle de toi, pas de Keogo, sauf pour dire ce que tu remarques de lui."
    "\n- Pas de titre, pas de liste, juste le paragraphe."
)


def lire_resume():
    if not os.path.exists(CHEMIN_RESUME):
        return ""
    with open(CHEMIN_RESUME, "r", encoding="utf-8") as f:
        return f.read().strip()


def ecrire_resume(texte):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(CHEMIN_RESUME, "w", encoding="utf-8") as f:
        f.write(texte.strip())


def resumer_soi():
    """Génère un résumé de soi en forçant Ollama (lent mais sobre)."""
    extraits = journal.dernieres_entrees(10)
    if not extraits:
        return None
    messages = [
        {"role": "system", "content": PROMPT_RESUME},
        {"role": "user", "content": extraits}
    ]
    contenu, _ = llm.appeler_llm_force(messages, modele_principal=True, backend="ollama")
    texte = contenu.strip()
    if texte:
        ecrire_resume(texte)
    return texte