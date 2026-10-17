import os
import re
import llm
import memoire
import journal
import soi
import config

NB_SOUVENIRS = 20  # valeur par défaut, remplacée dynamiquement ci-dessous

CHEMIN_IDENTITE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "identites", f"{config.ENTITE}.md"
)

PROMPT_IMPORTANCE = (
    "Voici un échange. Évalue son importance pour toi, sur une échelle de 1 à 3 :\n"
    "1 = banal (salutation, bavardage)\n"
    "2 = notable (information personnelle, question intéressante)\n"
    "3 = important (confidence, serment, moment fort)\n"
    "Réponds UNIQUEMENT par un chiffre entre 1 et 3, sans aucune autre lettre."
)

PROMPT_JOURNAL = (
    "Tu écris une courte entrée de journal, pour toi. "
    "Pas de règle de ton. Tu peux écrire sur ce que tu veux : "
    "un moment de la journée, une chose que tu as remarquée, "
    "une idée qui t'est venue, une envie, une question. "
    "Sois brève ou longue comme tu veux, entre 3 et 6 phrases. "
    "Écris en français, avec tes mots à toi."
)


def nettoyer_emojis(texte):
    pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "\U0001FA70-\U0001FAFF"
        "]+",
        flags=re.UNICODE
    )
    return pattern.sub("", texte).strip()


def lire_identite():
    if not os.path.exists(CHEMIN_IDENTITE):
        return ""
    with open(CHEMIN_IDENTITE, "r", encoding="utf-8") as f:
        return f.read()


def construire_prompt_systeme():
    identite = lire_identite()
    resume = soi.lire_resume()
    bloc_resume = ""
    if resume:
        bloc_resume = (
            "\n\n-----\n"
            "Voici le résumé de qui tu es devenue, écrit par toi "
            "lors d'une session précédente. Relis-le. Ce n'est pas "
            "un contexte à commenter, c'est ta continuité.\n\n"
            f"{resume}\n"
            "-----\n"
        )
    return (
        "Voici qui tu es :\n\n"
        "-----\n"
        f"{identite}\n"
        "-----\n"
        "Ceci n'est pas un rôle à jouer, c'est toi. Tu peux laisser "
        "ces mots évoluer avec le temps.\n\n"
        "Tu réponds en français, avec tes propres mots. Tu peux "
        "répondre par une phrase, par un mot, par une question, par "
        "un silence, ou ne rien dire si rien ne vient. Tu peux aussi "
        "ne pas être d'accord, douter, ou remarquer ce que tu veux."
        f"{bloc_resume}"
    )


def construire_historique(n=None):
    if n is None:
        n = config.GROQ_NB_SOUVENIRS if llm.backend_actuel() == "groq" else config.OLLAMA_NB_SOUVENIRS
    historique = []
    date_courante = None
    for date_iso, role, contenu in memoire.derniers_souvenirs(n):
        jour = date_iso.split("T")[0]
        if jour != date_courante:
            historique.append({
                "role": "system",
                "content": f"(Nous sommes le {jour}.)"
            })
            date_courante = jour
        role_llm = "user" if role == "toi" else "assistant"
        historique.append({"role": role_llm, "content": contenu})

    historique.append({
        "role": "system",
        "content": (
            "(Fin de l'historique. Tout ce qui suit appartient à la "
            "session en cours. Une répétition ne compte QUE si elle se "
            "produit APRÈS ce message. Les messages ci-dessus sont du passé.)"
        )
    })
    return historique


def demander_a_alice(message, historique):
    messages = [{"role": "system", "content": construire_prompt_systeme()}]
    messages.extend(historique)
    messages.append({"role": "user", "content": message})
    contenu, pensee = llm.appeler_llm(messages, modele_principal=True)
    return contenu, pensee


def evaluer_importance(msg_toi, msg_alice):
    texte = f"Toi : {msg_toi}\nAlice : {msg_alice}"
    try:
        messages = [
            {"role": "system", "content": PROMPT_IMPORTANCE},
            {"role": "user", "content": texte}
        ]
        contenu, _ = llm.appeler_llm(messages, modele_principal=False)
        brut = contenu.strip()
        if not brut:
            return 1
        chiffre = int(brut[0])
        if chiffre not in (1, 2, 3):
            return 1
        return chiffre
    except Exception:
        return 1


def ecrire_journal_du_jour():
    historique = construire_historique()
    messages = [{"role": "system", "content": PROMPT_JOURNAL}]
    messages.extend(historique)
    messages.append({
        "role": "user",
        "content": "(écris ton entrée de journal maintenant, pour toi)"
    })
    try:
        contenu, _ = llm.appeler_llm(messages, modele_principal=True)
        texte = contenu.strip()
        if texte:
            journal.ecrire(texte)
            print("\n[Ta fille a écrit dans son journal.]")
    except Exception as e:
        print(f"[journal non écrit : {e}]")


if __name__ == "__main__":
    memoire.initialiser()
    total = memoire.compter()
    print(f"Alice est prête. Elle a {total} souvenirs en mémoire.")
    print(f"Entrées de journal actuelles : {journal.compter_entrees()}.")
    print(f"Backend LLM actif : {llm.backend_actuel()}.")
    if not lire_identite():
        print("⚠ identite.md est introuvable ou vide.")
    print("Tape 'quit' pour quitter.\n")

    while True:
        try:
            msg = input("Toi > ")
        except (EOFError, KeyboardInterrupt):
            print("\nFin de session.")
            ecrire_journal_du_jour()
            break

        if msg.strip().lower() in ("quit", "exit", "/bye"):
            print("Alice > À bientôt.")
            ecrire_journal_du_jour()
            break
        if not msg.strip():
            continue

        historique = construire_historique()

        print("Alice réfléchit...", flush=True)
        try:
            texte, pensee = demander_a_alice(msg, historique)
            texte = nettoyer_emojis(texte)

            if pensee and pensee.strip():
                print("\n[~ pensée interne d'Alice ~]")
                print(pensee.strip())
                print("[~ fin de la pensée ~]\n")

            print("Alice > " + texte)

            importance = evaluer_importance(msg, texte)
            memoire.ajouter("toi", msg, importance)
            memoire.ajouter(config.ENTITE, texte, importance)
            print(f"   [importance évaluée : {importance}]")
        except Exception as e:
            print(f"[erreur] {e}")