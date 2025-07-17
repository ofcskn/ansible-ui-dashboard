import os
from app.config import Config
from flask import Flask
from flask_cors import CORS
from app.routes.playbooks_routes import playbooks_bp
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(playbooks_bp)

    return app
