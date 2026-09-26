# AI Engineering Assistant

Un assistant de diagnostic applicatif qui croise les logs, les configurations
JSON et un guide de migration pour produire un rapport argumenté et des actions
concrètes. Les outils locaux sont exposés par un serveur MCP en lecture seule.

## Cas de démonstration

L'application ne démarre plus après une migration de v1 vers v2. L'assistant doit
découvrir les fichiers, comparer les configurations et vérifier les règles de
migration pour expliquer le problème et proposer les vérifications nécessaires.

Les données fournies montrent que `auth_provider` disparaît de la configuration
v2 alors que le guide le rend obligatoire. Le délai passe de 30 à 60 secondes et
`max_connections` est ajouté avec la valeur 100. Les logs signalent un échec de
chargement du fournisseur d'authentification.

Les sources utilisent des noms différents : `auth.provider` dans les logs,
`auth_provider` dans les configurations et le guide, et `auth.mode` pour le
paramètre obsolète, distinct de `auth_mode`. L'assistant doit signaler cette
ambiguïté et proposer de vérifier le schéma de l'application.

## Organisation

```text
ai-engineering-assistant/
├── agent/
│   ├── agent.py
│   └── prompts.py
├── mcp_server/
│   ├── server.py
│   └── tools/
│       ├── logs.py
│       ├── configs.py
│       ├── documentation.py
│       └── files.py
├── data/
│   ├── application.log
│   ├── config_v1.json
│   ├── config_v2.json
│   └── migration_guide.txt
├── .vscode/mcp.json
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Cette arborescence est installée à la racine du dépôt existant. Le nom du dossier
local peut être changé en `ai-engineering-assistant` sans modifier le code.

## Installation

Python 3.11 ou supérieur. Depuis la racine du dépôt :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env  # uniquement si vous n'avez pas déjà de .env
```

Renseigner `HUGGINGFACEHUB_API_TOKEN` dans `.env`. `HF_MODEL_ID` permet de changer
le modèle ; sa valeur par défaut est `openai/gpt-oss-20b`. Le compte Hugging Face
doit avoir accès à un fournisseur d'inférence compatible avec ce modèle et les
appels d'outils. La disponibilité et les frais dépendent du fournisseur.

## Utilisation

```bash
# Rapport de migration sur les données de démonstration
python -m agent.agent

# Investigation ciblée
python -m agent.agent "Pourquoi l'application ne démarre-t-elle plus ? Cite tes sources."

# Serveur seul, pour un client MCP stdio
python -m mcp_server.server
```

L'agent démarre le serveur avec le même interpréteur Python et ferme la session
MCP après l'analyse, y compris en cas d'erreur. Le serveur peut aussi être lancé
depuis la configuration `.vscode/mcp.json` (interpréteur Linux/macOS ; sous Windows,
adapter le chemin en `.venv/Scripts/python.exe`).

## Outils

| Outil | Fonction |
| --- | --- |
| `list_project_files` | Découvrir les fichiers sous `data/` |
| `read_project_file` | Lire un fichier texte UTF-8 |
| `analyze_logs` | Extraire les lignes WARNING et ERROR |
| `compare_configs` | Comparer les clés JSON ajoutées, supprimées ou modifiées |
| `search_documentation` | Trouver les paragraphes du guide par mots-clés |

Les chemins relatifs partent de la racine du projet, indépendamment du répertoireJ
courant du serveur. L'accès est limité à `data/`, y compris pour les liens
symboliques. Les objets JSON imbriqués sont comparés comme des valeurs complètes.
La recherche documentaire utilise les mots-clés du guide anglais, sans recherche
sémantique. Le modèle interprète les résultats et rédige le rapport ; les outils
n'appliquent aucune modification. Les extraits consultés sont envoyés au modèle
hébergé : utiliser des données adaptées à ce traitement.

