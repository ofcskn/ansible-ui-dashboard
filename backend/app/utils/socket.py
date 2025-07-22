import socket
import json

from app.config import Config

def call_userenvd(username: str):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(Config.RAW_SOCKET_PATH)
        client.send(json.dumps({"username": username}).encode())
        response = client.recv(4096).decode()
        client.close()
        return True, json.loads(response)
    except Exception as e:
        return False, f"Failed to contact userenvd: {str(e)}"
