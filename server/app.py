from flask import Flask
from flask_restx import Api
from api.student import api as students
from db.db import init_db
from flask_cors import CORS
from flask import request

app = Flask(__name__)

# Note that I'm currently hard-coding the IP addresses of the frontend
# for simplicity for the in-class exercise
# this should be an environment variable in a real-world scenario
# and should be set to the IP address of the frontend
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:8000",
                "http://10.228.141.212:8000",
            ],  # Get origin from env with fallback
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    },
)


init_db(app)

# Initialize Flask-RESTx API and register the students namespace
api = Api(app)
api.add_namespace(students)  # Add the students namespace to the API

# uncomment for debugging the request headers if things are not working
# @app.before_request
# def log_request_info():
#     print(f"Request Headers: {request.headers}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6969)
