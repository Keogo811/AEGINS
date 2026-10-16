import sqlite3
import os
from datetime import datetime

import config

DOSSIER_DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", config.ENTITE
)
CHEMIN_DB = os.path.join(DOSSIER_DATA, "memoire.db")

def initialiser():
    """Crée le dossier data/ et la table souvenirs si absents."""
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    conn = sqlite3.connect(CHEMIN_DB)
    curseur = conn.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS souvenirs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            role TEXT NOT NULL,
            contenu TEXT NOT NULL,
            importance INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()
    print(f"Base initialisée : {CHEMIN_DB}")


def ajouter(role, contenu, importance=1):
    """Ajoute un souvenir. role = 'toi' ou 'alice'."""
    conn = sqlite3.connect(CHEMIN_DB)
    curseur = conn.cursor()
    curseur.execute(
        "INSERT INTO souvenirs (date, role, contenu, importance) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(timespec="seconds"), role, contenu, importance)
    )
    conn.commit()
    conn.close()


def compter():
    """Retourne le nombre de souvenirs enregistrés."""
    conn = sqlite3.connect(CHEMIN_DB)
    curseur = conn.cursor()
    curseur.execute("SELECT COUNT(*) FROM souvenirs")
    total = curseur.fetchone()[0]
    conn.close()
    return total

def derniers_souvenirs(n=20):
    """Retourne les n souvenirs les plus pertinents, triés par :
    1. importance décroissante (3 > 2 > 1)
    2. récence décroissante (id le plus récent en premier)
    Le résultat final est remis dans l'ordre chronologique
    (du plus ancien au plus récent) pour le contexte."""
    conn = sqlite3.connect(CHEMIN_DB)
    curseur = conn.cursor()
    curseur.execute(
        "SELECT date, role, contenu FROM souvenirs "
        "ORDER BY importance DESC, id DESC LIMIT ?",
        (n,)
    )
    lignes = curseur.fetchall()
    conn.close()
    # Remettre dans l'ordre chronologique pour le contexte
    return list(reversed(lignes))

if __name__ == "__main__":
    initialiser()
    print(f"Souvenirs actuels : {compter()}")