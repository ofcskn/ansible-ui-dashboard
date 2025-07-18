
import os

PLAYBOOKS_DIR = os.getenv("PLAYBOOKS_DIR", "playbooks")
REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
REDIS_PORT=os.getenv("REDIS_PORT", 6379)