import eventlet
eventlet.monkey_patch() 

import os
from app import create_app
from app.config import Config
from dotenv import load_dotenv
from app.extensions import socketio

load_dotenv() 
app = create_app()
if __name__ == "__main__":
    socketio.run(app, debug=True, host=Config.FLASK_HOST, port=Config.FLASK_PORT)