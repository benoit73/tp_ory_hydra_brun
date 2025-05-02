# 🛡️ API Flask protégée par Ory Hydra

Ce projet est une démonstration d'une API Flask sécurisée avec des jetons OAuth 2.0 (JWT) générés par Ory Hydra.
## 📦 Prérequis

    Python 3.8+

    Docker + Docker Compose

    pip (installateur de paquets Python)

## ⚙️ Installation
### 1. Cloner les dépôts

Clonez le dépôt d’Ory Hydra :

git clone https://github.com/ory/hydra.git
cd hydra
git checkout v2.3.0

Clonez votre API Flask :

cd ..
git clone https://github.com/benoit73/tp_ory_hydra_brun.git
cd tp_ory_hydra_brun

### 2. Lancer Hydra

Dans le dossier hydra, démarrez Hydra avec Docker :

docker compose -f quickstart.yml -f quickstart-postgres.yml up --build

### 3. Créer un client OAuth2

Dans un autre terminal :

docker compose -f quickstart.yml exec hydra \
  hydra create oauth2-client \
  --endpoint http://127.0.0.1:4445/ \
  --id my-api-client \
  --secret my-api-secret \
  --grant-type client_credentials \
  --scope openid

### 4. Démarrer l’API Flask

Depuis le dossier tp_ory_hydra_brun :

pip install -r requirements.txt
python3 app.py

### 🚀 Endpoints disponibles
GET /get_jwt

Retourne un JWT généré automatiquement via Hydra à l’aide des identifiants stockés dans .env.

curl http://localhost:5000/get_jwt

GET /protected

Accède à une route protégée avec un JWT transmis dans l’en-tête jwt.

curl -H "jwt: <votre_token>" http://localhost:5000/protected

## 🔍 Comment ça marche ?

    L’API appelle /oauth2/token de Hydra pour récupérer un JWT.

    Le client peut utiliser ce token pour interroger /protected.

    L’API appelle /oauth2/introspect de Hydra pour vérifier la validité du token.

