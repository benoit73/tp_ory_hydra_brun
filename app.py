from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import base64
import requests
import os

load_dotenv()
HYDRA_TOKEN_URL = os.getenv("HYDRA_TOKEN_URL")
HYDRA_INTROSPECT_URL = os.getenv("HYDRA_INTROSPECT_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

def introspect_token(token):
    print(token)
    response = requests.post(
        HYDRA_INTROSPECT_URL,
        data={"token": token},
    )
    if response.status_code == 200:
        return response.json()
    return {"active": False}

@app.route("/protected")
def protected():
    auth_header = request.headers.get("jwt")
    if not auth_header:
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header
    introspection = introspect_token(token)

    if introspection.get("active"):
        return jsonify({"message": "Access granted", "token_info": introspection})
    else:
        return jsonify({"error": "Invalid or expired token"}), 401

@app.route("/get_jwt")
def get_jwt_from_hydra():
    response = requests.post(
        HYDRA_TOKEN_URL,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "client_credentials",
            "scope": "openid"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Erreur récupération token :", response.text)
        return None
    
@app.route("/")
def index():
    return "API Flask protégée par Hydra"

if __name__ == "__main__":
    app.run(debug=True)
