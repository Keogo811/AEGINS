from flask import Flask, render_template, request, jsonify
import memoire
import alice

app = Flask(__name__)

memoire.initialiser()


@app.route("/")
def accueil():
    total = memoire.compter()
    return render_template("index.html", total=total)


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
        return jsonify({"ok": True, "message": "Alice a écrit dans son journal."})
    except Exception as e:
        return jsonify({"ok": False, "message": f"Erreur : {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)