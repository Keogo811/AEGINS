import os
from datetime import datetime

import config

DOSSIER_DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", config.ENTITE
)
CHEMIN_JOURNAL = os.path.join(DOSSIER_DATA, "journal.md")


def ecrire(texte, marqueur=None):
    """Ajoute une entrée horodatée à la fin du journal.
    Le marqueur optionnel (ex: 'rumination') apparaît dans le titre."""
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M")
    suffixe = f" [{marqueur}]" if marqueur else ""
    with open(CHEMIN_JOURNAL, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n## {horodatage}{suffixe}\n\n{texte.strip()}\n")


def compter_entrees():
    """Retourne le nombre d'entrées (séparateurs '---')."""
    if not os.path.exists(CHEMIN_JOURNAL):
        return 0
    with open(CHEMIN_JOURNAL, "r", encoding="utf-8") as f:
        return f.read().count("\n---\n")
    
def dernieres_entrees(n=2):
    """Retourne les n dernières entrées du journal, du plus ancien au plus récent."""
    if not os.path.exists(CHEMIN_JOURNAL):
        return ""
    with open(CHEMIN_JOURNAL, "r", encoding="utf-8") as f:
        contenu = f.read()
    blocs = [b.strip() for b in contenu.split("\n---\n") if b.strip()]
    return "\n\n---\n\n".join(blocs[-n:])