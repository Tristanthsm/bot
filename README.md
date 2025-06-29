# Workflow de raccourcissement d'URL

Ce dépôt contient un fichier `workflow.json` pour n8n. Il permet de raccourcir des URLs à l'aide d'Airtable et expose trois webhooks :

- `/sh` : crée un lien court en recevant une URL en paramètre `url`.
- `/go` : redirige vers l'URL d'origine via le paramètre `id`.
- `/dashboard` : renvoie quelques statistiques sur les liens existants.

## Import du workflow

1. Ouvrez l'interface n8n.
2. Dans le menu principal, choisissez **Import** puis sélectionnez le fichier `workflow.json` présent dans ce dépôt.
3. Pensez à renseigner dans chaque noeud Airtable votre **Base ID** et le **nom de la table**.
4. Configurez les identifiants Airtable via la section **Credentials** de n8n (clé API ou token).

## Exemple d'appel du webhook

Pour créer une URL courte :

```bash
curl "https://<votre-instance-n8n>/webhook/sh?url=https://exemple.com"
```

La réponse contiendra l'identifiant et l'URL raccourcie retournés par le workflow.

## Prérequis

- Une instance n8n fonctionnelle.
- Un compte Airtable avec une clé API ou un token d'accès personnel.
- Une base Airtable contenant la table que vous souhaitez utiliser pour stocker les liens.
- Facultatif : configurez la variable d'environnement `WEBHOOK_URL` de n8n si vous utilisez un domaine personnalisé.


## Bot de trading

Ce dépôt propose également un exemple de **bot de trading** écrit en Python (`trading_bot.py`).
Il s'agit d'une ébauche reposant sur la librairie `yfinance` pour récupérer les cours
boursiers en temps réel. Le programme analyse les données à l'aide d'une stratégie
simple de croisements de moyennes mobiles pour générer des signaux **BUY** ou **SELL**.
Chaque signal déclenche l'envoi d'une notification (fonctionalité à personnaliser
selon vos besoins).

Pour l'exécuter :

```bash
pip install -r requirements.txt
python trading_bot.py
```

Le bot télécharge les cours de l'action `AAPL` toutes les minutes et affiche les
signaux détectés. Vous pouvez adapter la logique d'analyse et les notifications en
modifiant le fichier `trading_bot.py`.
