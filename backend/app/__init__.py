from flask import Flask
from flask_cors import CORS
from app.routes.playbooks import playbooks_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(playbooks_bp)

    return app
