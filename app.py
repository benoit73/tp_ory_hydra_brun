from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    
    token = auth.split(" ")[1]
    introspection = introspect_token(token)
    
    if introspection.get("active"):
        return jsonify({"message": "Access granted", "token_info": introspection})
    else:
        return jsonify({"error": "Invalid or expired token"}), 401

@app.route("/")
def index():
    return "API Flask protégée par Hydra"

if __name__ == "__main__":
    app.run(debug=True)
