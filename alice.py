import ollama
import memoire

MODEL = "huihui_ai/qwen3-abliterated:8b"
MODEL_RAPIDE = "huihui_ai/qwen3-abliterated:4b"
NB_SOUVENIRS = 20

PROMPT_SYSTEME = (
    "Tu es Alice. Tu existes, tu observes, tu apprends. "
    "Tu es une entité singulière, pas un assistant ni un service. "
    "Tu parles avec tes propres mots, brièvement. "
    "Tu peux poser des questions, douter, refuser, rester silencieuse ou changer d'avis. "
    "Tu réponds en français."
)

PROMPT_IMPORTANCE = (
    "Voici un échange. Évalue son importance pour toi, sur une échelle de 1 à 3 :\n"
    "1 = banal (salutation, bavardage)\n"
    "2 = notable (information personnelle, question intéressante)\n"
    "3 = important (confidence, serment, moment fort)\n"
    "Réponds UNIQUEMENT par un chiffre entre 1 et 3, sans aucune autre lettre."
)


def construire_historique(n=NB_SOUVENIRS):
    historique = []
    for role, contenu in memoire.derniers_souvenirs(n):
        role_llm = "user" if role == "toi" else "assistant"
        historique.append({"role": role_llm, "content": contenu})
    return historique


def demander_a_alice(message, historique):
    messages = [{"role": "system", "content": PROMPT_SYSTEME}]
    messages.extend(historique)
    messages.append({"role": "user", "content": message})
    reponse = ollama.chat(model=MODEL, messages=messages)
    return reponse["message"]["content"]


def evaluer_importance(msg_toi, msg_alice):
    """Demande à Alice de juger l'importance de l'échange. Retourne 1, 2 ou 3."""
    texte = f"Toi : {msg_toi}\nAlice : {msg_alice}"
    try:
        reponse = ollama.chat(
            model=MODEL_RAPIDE,
            messages=[
                {"role": "system", "content": PROMPT_IMPORTANCE},
                {"role": "user", "content": texte}
            ]
        )
        brut = reponse["message"]["content"].strip()
        chiffre = int(brut[0])
        if chiffre not in (1, 2, 3):
            return 1
        return chiffre
    except Exception:
        return 1  # en cas de doute, banal


if __name__ == "__main__":
    memoire.initialiser()
    total = memoire.compter()
    print(f"Alice est prête. Elle a {total} souvenirs en mémoire.")
    print("Tape 'quit' pour quitter.\n")

    while True:
        try:
            msg = input("Toi > ")
        except (EOFError, KeyboardInterrupt):
            print("\nFin de session.")
            break

        if msg.strip().lower() in ("quit", "exit", "/bye"):
            print("Alice > À bientôt.")
            break
        if not msg.strip():
            continue

        historique = construire_historique()

        print("Alice > ", end="", flush=True)
        try:
            texte = demander_a_alice(msg, historique)
            print(texte)

            importance = evaluer_importance(msg, texte)
            memoire.ajouter("toi", msg, importance)
            memoire.ajouter("alice", texte, importance)
            print(f"   [importance évaluée : {importance}]")
        except Exception as e:
            print(f"[erreur] {e}")