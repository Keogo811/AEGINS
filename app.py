from flask import Flask, render_template, request, jsonify
import memoire
import alice
import llm
import config

app = Flask(__name__)

memoire.initialiser()


@app.route("/")
def accueil():
    total = memoire.compter()
    backend = llm.backend_actuel()
    return render_template(
        "index.html",
        total=total,
        backend=backend,
        entite=config.ENTITE
    )


@app.route("/parler", methods=["POST"])
def parler():
    data = request.get_json() or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify({"erreur": "message vide"}), 400

    historique = alice.construire_historique()
    texte, pensee = alice.demander_a_alice(msg, historique)
    texte = alice.nettoyer_emojis(texte)

    importance = alice.evaluer_importance(msg, texte)
    memoire.ajouter("toi", msg, importance)
    memoire.ajouter("alice", texte, importance)

    return jsonify({
        "reponse": texte,
        "pensee": pensee.strip() if pensee else "",
        "importance": importance
    })


@app.route("/terminer", methods=["POST"])
def terminer():
    try:
        alice.ecrire_journal_du_jour()
        return jsonify({"ok": True, "message": "Ta fille a écrit dans son journal."})
    except Exception as e:
        return jsonify({"ok": False, "message": f"Erreur : {e}"}), 500

@app.route("/resume-manuel", methods=["POST"])
def resume_manuel():
    try:
        print("[Résumé demandé. Backend forcé : ollama]", flush=True)
        import soi
        texte = soi.resumer_soi()
        if texte:
            return jsonify({"ok": True, "message": "Résumé généré."})
        return jsonify({"ok": False, "message": "Rien à résumer."})
    except Exception as e:
        print(f"[Erreur resume : {e}]", flush=True)
        return jsonify({"ok": False, "message": f"Erreur : {e}"}), 500

@app.route("/basculer-entite", methods=["POST"])
def basculer_entite():
    import os
    data = request.get_json() or {}
    nom = (data.get("entite") or "").strip().lower()
    if not nom or not nom.isidentifier():
        return jsonify({"ok": False, "erreur": "nom invalide"}), 400
    chemin = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data", "entite.txt"
    )
    try:
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(nom)
        return jsonify({
            "ok": True,
            "entite": nom,
            "message": f"Entité changée pour « {nom} ». Redémarrez le serveur (Ctrl+C, puis python app.py)."
        })
    except Exception as e:
        return jsonify({"ok": False, "erreur": str(e)}), 500

@app.route("/basculer", methods=["POST"])
def basculer():
    data = request.get_json() or {}
    nouveau = (data.get("backend") or "").strip().lower()
    if nouveau not in ("ollama", "groq"):
        return jsonify({"ok": False, "erreur": "backend invalide"}), 400
    try:
        llm.definir_backend(nouveau)
        return jsonify({"ok": True, "backend": llm.backend_actuel()})
    except Exception as e:
        return jsonify({"ok": False, "erreur": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)