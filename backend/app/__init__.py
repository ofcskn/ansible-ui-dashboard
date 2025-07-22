import os
from app.config import Config
from flask import Flask
from flask_cors import CORS
from app.routes.playbooks_routes import playbooks_bp
from app.routes.user_routes import users_bp
from app.extensions import db, migrate, socketio
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)

    jwt = JWTManager(app)

    socketio.init_app(app) 

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(playbooks_bp)
    app.register_blueprint(users_bp)

    return app
