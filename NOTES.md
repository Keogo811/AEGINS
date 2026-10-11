# Notes personnelles — Projekt AEGINS

## Lancer Alice sur le PC

```
cd C:\Users\aegin\AEGINS
python app.py
```

Puis ouvrir dans le navigateur : `http://127.0.0.1:5000`

Pour arrêter : `Ctrl + C` dans PowerShell.

## Utiliser Alice depuis le téléphone (même WiFi que le PC)

1. Vérifier que PC et téléphone sont sur la même box (téléphone en WiFi, pas en 4G).
2. Sur le PC, dans PowerShell : `ipconfig`
3. Repérer la ligne **Adresse IPv4** de la carte connectée. Ex : `192.168.1.92`
4. Lancer le serveur : `python app.py`
5. Sur le téléphone, ouvrir : `http://[IP]:5000` (ex : `http://192.168.1.92:5000`)

Si Windows demande l'autorisation, accepter sur **réseaux privés uniquement**.

## Terminer une session

Cliquer sur le bouton **TERMINER** dans la barre du bas.
Alice écrit alors une entrée dans `data/journal.md`.

## Fichiers importants

- `alice.py` : le cerveau d'Alice (dialogue, mémoire, journal).
- `memoire.py` : gestion des souvenirs (SQLite, `data/alice.db`).
- `journal.py` : écriture du journal (`data/journal.md`).
- `app.py` : serveur web Flask.
- `identite.md` : qui est Alice. Modifiable à la main.
- `data/` : **local et privé**, jamais envoyé sur GitHub.

## Sauvegarder / restaurer

- Après chaque session importante : `git add . ; git commit -m "..." ; git push`
- Revenir à une version antérieure : `git log --oneline` puis `git checkout [hash]`

## Polices

Cinzel (titres) + EB Garamond (texte), chargées depuis Google Fonts.
Nécessite internet la première fois, puis mise en cache.