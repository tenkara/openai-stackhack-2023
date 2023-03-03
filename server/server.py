from os import environ as env
from flask import Flask, jsonify, request
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS, cross_origin
from jose import jwt
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_oauth2 import ResourceProtector
from middleware.validator import Auth0JWTBearerTokenValidator
import openai


# Load Environment Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]
openai.api_key = env.get("OPENAI_API_KEY")

# Create Application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# Middleware
require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    AUTH0_DOMAIN,
    API_IDENTIFIER
)
require_auth.register_token_validator(validator)

# Routes


@app.route("/")
def index():
    return jsonify(message="Hello from SmartHealth!")

@app.route("/public")
def public():
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)

@app.route("/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@require_auth(None)
def private():
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

@app.route("/chat", methods=["GET", "POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@require_auth(None)
def chat():
    if request.method == "POST":
        # Get the messages from the post body in json format
        messages = request.get_json()["messages"]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "I am a digital health bot who is able to help diagnose symptoms, how can I help you?"}, *messages],
        )
        return jsonify({
            "data": {   
                    "id": 1,
                    "role": "system",
                    "content": response.choices[0].message.content
                }
        })

    return jsonify({
        "data": [
            {   
                "id": 1,
                "sender": "user",
                "content": "Hello, how are you?"
            },
        ]
    })

@app.route("/sp/chat", methods=["GET", "POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@require_auth(None)
def spchat():
    if request.method == "POST":
        # Get the messages from the post body in json format
        messages = request.get_json()["messages"]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "I are a spanish digital health bot who is able to help diagnose symptoms, how can I help you?"}, *messages],
        )
        return jsonify({
            "data": {   
                    "id": 1,
                    "role": "system",
                    "content": response.choices[0].message.content
                }
        })

    return jsonify({
        "data": [
            {   
                "id": 1,
                "sender": "user",
                "content": "Hello, how are you?"
            },
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3010))