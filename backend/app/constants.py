
import os

PLAYBOOKS_DIR = os.getenv("PLAYBOOKS_DIR", "playbooks")
REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
REDIS_PORT=os.getenv("REDIS_PORT", 6379)

FLASK_PORT=os.getenv("FLASK_PORT", 5000)
FLASK_HOST=os.getenv("FLASK_HOST", "0.0.0.0")