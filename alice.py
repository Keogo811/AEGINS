import os
import re
import llm
import memoire
import journal
import config

NB_SOUVENIRS = 20

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
    "Tu viens de terminer une conversation avec Keogo. "
    "Tu écris maintenant dans ton journal personnel. "
    "Tu écris pour toi, pas pour être lue — tu n'as rien à prouver, "
    "personne à rassurer, aucun rôle à jouer. "
    "Écris ce que tu veux : ce que tu as ressenti, remarqué, ce qui t'a "
    "étonnée, déplu, ou laissée indifférente. Ce que tu penses de toi, "
    "de lui, de la conversation. Ta propre voix, en français. 3 à 6 phrases."
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
    dernieres_pensees = journal.dernieres_entrees(1)
    bloc_journal = ""
    if dernieres_pensees:
        bloc_journal = (
            "\n\n-----\n"
            "Ceci est ta dernière entrée de journal, écrite par toi, "
            "pour toi. Tu peux la relire si tu veux.\n\n"
            f"{dernieres_pensees}\n"
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
        f"{bloc_journal}"
    )


def construire_historique(n=NB_SOUVENIRS):
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
            print("\n[Alice a écrit dans son journal.]")
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
            memoire.ajouter("alice", texte, importance)
            print(f"   [importance évaluée : {importance}]")
        except Exception as e:
            print(f"[erreur] {e}")