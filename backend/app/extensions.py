from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)
socketio = SocketIO(cors_allowed_origins="*")