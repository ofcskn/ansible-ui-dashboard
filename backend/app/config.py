import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    PLAYBOOKS_DIR = os.getenv("PLAYBOOKS_DIR", "playbooks")

    REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT=os.getenv("REDIS_PORT", 6379)

    FLASK_PORT=os.getenv("FLASK_PORT", 5000)
    FLASK_HOST=os.getenv("FLASK_HOST", "0.0.0.0")

    USER_WORKSPACE_ROOT=os.getenv("USER_WORKSPACE_ROOT", "/opt/users")
    RAW_SOCKET_PATH=os.getenv("OPERATIONS_SOCKET_PATH", "/var/run/userenvd/socket")