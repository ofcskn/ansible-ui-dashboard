from app.constants import REDIS_HOST, REDIS_PORT
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)