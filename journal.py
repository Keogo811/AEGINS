import os
from datetime import datetime

DOSSIER_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CHEMIN_JOURNAL = os.path.join(DOSSIER_DATA, "journal.md")


def ecrire(texte):
    """Ajoute une entrée horodatée à la fin du journal."""
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CHEMIN_JOURNAL, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n## {horodatage}\n\n{texte.strip()}\n")


def compter_entrees():
    """Retourne le nombre d'entrées (séparateurs '---')."""
    if not os.path.exists(CHEMIN_JOURNAL):
        return 0
    with open(CHEMIN_JOURNAL, "r", encoding="utf-8") as f:
        return f.read().count("\n---\n")