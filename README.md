# Intégration OAuth2 avec ORY Hydra et Flask

**Auteur** : Benoit MATHIEZ

## 🛠️ Étapes d'installation

### 1. Cloner le dépôt d'Ory Hydra

git clone https://github.com/ory/hydra.git
cd hydra
git checkout v2.3.0

### 2. Démarrer l’API Flask

Dans un autre dossier :

git clone https://github.com/benoit73/tp_ory_hydra_brun.git
cd tp_ory_hydra_brun
python3 app.py

### 3. Démarrer les services Hydra avec Docker Compose

cd ../hydra
docker compose -f quickstart.yml \
  -f quickstart-postgres.yml \
  up \
  --build

### 4. Enregistrer une nouvelle application (notre API)

docker compose -f quickstart.yml exec hydra \
  hydra create oauth2-client \
  --endpoint http://127.0.0.1:4445/ \
  --id my-api-client \
  --secret my-api-secret \
  --grant-type client_credentials \
  --scope openid,offline

### 5. Générer un JWT

curl -X POST http://localhost:4444/oauth2/token \
  -u my-api-client:my-api-secret \
  -d "grant_type=client_credentials" \
  -d "scope=openid"

Copiez le token (access_token) renvoyé dans la réponse JSON.
### 6. Faire une requête à l’API Flask avec le token

curl -H "Authorization: Bearer <monToken>" http://localhost:5000/protected

## 🧠 Comment ça marche ?

ORY Hydra ne gère pas l’authentification elle-même, mais orchestre les flux OAuth2/OpenID Connect. Voici les étapes du processus :

    L’application front demande à se connecter (ex. /oauth2/auth)

    Hydra redirige vers une application de login personnalisée

    Cette application vérifie les identifiants → informe Hydra que l’utilisateur est authentifié

    Hydra redirige vers l’application avec un code d’autorisation

    L’application échange ce code contre un access token (JWT)

    Le front ou le back utilise ce token pour appeler une API

    L’API vérifie la signature du token via la clé publique d’Hydra (ou utilise l’endpoint /introspect)

