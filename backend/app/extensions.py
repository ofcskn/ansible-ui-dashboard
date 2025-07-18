from app.constants import REDIS_HOST, REDIS_PORT
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
socketio = SocketIO(cors_allowed_origins="*")