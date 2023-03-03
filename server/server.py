from os import environ as env
from flask import Flask, jsonify
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from flask_cors import cross_origin
from jose import jwt
from flask_sqlalchemy import SQLAlchemy

# Create Application
app = Flask(__name__)

# Load Environment Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]

# Middleware
from middleware.auth import requires_auth, AuthError

# Routes

# Controllers API
@app.route("/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@app.route("/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth
def private():
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)


@app.route("/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3000"])
@requires_auth
def private_scoped():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3010))