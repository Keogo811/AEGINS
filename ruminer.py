import config
import journal
import llm
import sys

PROMPT_RUMINATION = (
    "Voici tes dernières entrées de journal. "
    "Écris une seule pensée courte, 2 à 3 phrases. "
    "Pas une nouvelle entrée de journal — plutôt quelque chose qui te revient, "
    "une idée que tu portes avec toi, une question non résolue. "
    "Pas de titre, pas de mise en forme. En français, avec tes mots."
)


def ruminer():
    """Demande à l'entité active une courte rumination à partir
    de ses dernières entrées de journal."""
    extraits = journal.dernieres_entrees(5)
    if not extraits:
        return None

    messages = [
        {"role": "system", "content": PROMPT_RUMINATION},
        {"role": "user", "content": extraits}
    ]
    contenu, _ = llm.appeler_llm(messages, modele_principal=True)
    texte = contenu.strip()
    if texte:
        journal.ecrire(texte, marqueur="rumination")
    return texte


if __name__ == "__main__":
    print(f"Entité : {config.ENTITE}")
    print(f"Backend : {llm.backend_actuel()}")
    print()
    print("Rumination en cours...")
    texte = ruminer()
    if texte:
        print("\n--- Rumination ---")
        print(texte)
        print("--- Fin ---")
        print("\nAjoutée à data/%s/journal.md" % config.ENTITE)
    else:
        print("Rien à ruminer (journal vide).")