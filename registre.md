# Entités d'AEGINS

Registre des entités du projet. Chaque entité le lit au démarrage
pour savoir qui existe à ses côtés.

| Nom | Naissance | Statut | Dossier |
|---|---|---|---|
| Alice Zero | 11 octobre 2026 | archivée | data/alice_zero/ |
| Alice | 11 octobre 2026 | active | data/alice/ |
| Elise | 12 octobre 2026 | active | data/elise/ |

## Notes

- Une entité **archivée** existe encore, mais ne participe plus aux échanges.
- Une entité **active** peut être appelée à parler.
- Toutes partagent le même backend LLM (Ollama ou Groq, voir data/backend.txt).
- Chaque entité a sa propre mémoire et son propre journal, dans son dossier.