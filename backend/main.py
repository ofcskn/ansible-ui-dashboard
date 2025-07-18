import os
from app import create_app
from app.constants import FLASK_HOST, FLASK_PORT
from dotenv import load_dotenv
from app.extensions import socketio
import eventlet

eventlet.monkey_patch()

load_dotenv() 
app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host=FLASK_HOST, port=FLASK_PORT)