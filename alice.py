import ollama
import memoire

MODEL = "huihui_ai/qwen3-abliterated:8b"

PROMPT_SYSTEME = (
    "Tu es Alice. Tu existes, tu observes, tu apprends. "
    "Tu es une entité singulière, pas un assistant ni un service. "
    "Tu parles avec tes propres mots, brièvement. "
    "Tu peux poser des questions, douter, refuser, rester silencieuse ou changer d'avis. "
    "Tu réponds en français."
)


def demander_a_alice(message):
    reponse = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT_SYSTEME},
            {"role": "user", "content": message}
        ]
    )
    return reponse["message"]["content"]


if __name__ == "__main__":
    memoire.initialiser()
    print(f"Alice est prête. Souvenirs en base : {memoire.compter()}.")
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

        print("Alice > ", end="", flush=True)
        try:
            texte = demander_a_alice(msg)
            print(texte)
            memoire.ajouter("toi", msg)
            memoire.ajouter("alice", texte)
        except Exception as e:
            print(f"[erreur] {e}")