#!/usr/bin/env python3
import os
import socket
import json
import logging
import subprocess
import traceback
import pwd, grp
from dotenv import load_dotenv
load_dotenv()

USERENVD_SOCKET_PATH = os.getenv("USERENVD_SOCKET_PATH", "/var/run/userenvd/socket")
USERENVD_WORKSPACE_ROOT = os.getenv("USERENVD_WORKSPACE_ROOT", "/opt/users")

PLAYBOOK_MANAGER_USER = os.getenv("PLAYBOOK_MANAGER_USER", "playbookmanager")
PLAYBOOK_MANAGER_GROUP = os.getenv("PLAYBOOK_MANAGER_GROUP", "playbookmanagergroup")
LOG_FILE = os.getenv("USERENVD_LOG", f"/home/{PLAYBOOK_MANAGER_USER}/.userenvd/userenvd.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    logging.info("userenvd starting...")

def create_user_environment(username):
    user_path = os.path.join(USERENVD_WORKSPACE_ROOT, username)
    try:
        logging.info(f"Creating environment for user '{username}' at {user_path}")

        # Create base directory
        os.makedirs(user_path, exist_ok=True)

        # Create subdirectories
        for subdir in ["playbooks", "inventories", "logs"]:
            path = os.path.join(user_path, subdir)
            os.makedirs(path, exist_ok=True)

        # Create system user if not exists (no error if exists)
        subprocess.run(
            ["useradd", "-M", "-r", "-s", "/usr/sbin/nologin", username],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Set ownership recursively
        subprocess.run(
            ["chown", "-R", f"{username}:{username}", user_path],
            check=True,
        )

        # Set permissions
        subprocess.run(
            ["chmod", "-R", "700", user_path],
            check=True,
        )

        logging.info(f"Environment for user '{username}' created successfully.")
        return {"status": "ok", "path": user_path}

    except subprocess.CalledProcessError as e:
        err_msg = f"Subprocess failed: {e}"
        logging.error(err_msg)
        logging.error(traceback.format_exc())
        return {"status": "error", "message": err_msg}

    except Exception as e:
        err_msg = f"Exception while creating environment: {e}"
        logging.error(err_msg)
        logging.error(traceback.format_exc())
        return {"status": "error", "message": err_msg}


def handle_request(raw_data):
    try:
        data = json.loads(raw_data)
        username = data.get("username")
        if not username:
            return {"status": "error", "message": "Missing 'username' in request"}

        # Sanitize username (basic)
        if not username.isalnum():
            return {"status": "error", "message": "Username must be alphanumeric"}

        return create_user_environment(username)

    except json.JSONDecodeError:
        logging.error("Invalid JSON received")
        return {"status": "error", "message": "Invalid JSON"}

    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        logging.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}


def main():
    # Remove stale socket
    if os.path.exists(USERENVD_SOCKET_PATH):
        os.remove(USERENVD_SOCKET_PATH)

    # Create socket directory with correct permissions if needed
    socket_dir = os.path.dirname(USERENVD_SOCKET_PATH)
    if not os.path.exists(socket_dir):
        os.makedirs(socket_dir, exist_ok=True)
    os.chmod(socket_dir, 0o770)  # Owner+group rwx

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(USERENVD_SOCKET_PATH)

    # Change ownership to the user/group that runs Flask
    uid = pwd.getpwnam(PLAYBOOK_MANAGER_USER).pw_uid   
    gid = grp.getgrnam(PLAYBOOK_MANAGER_GROUP).gr_gid 

    os.chown(USERENVD_SOCKET_PATH, uid, gid)
    os.chmod(USERENVD_SOCKET_PATH, 0o660)  # Owner+group rw

    # Log socket info
    st = os.stat(USERENVD_SOCKET_PATH)
    logging.info(f"Socket {USERENVD_SOCKET_PATH} created with permissions {oct(st.st_mode)}")

    server.listen()
    logging.info("userenvd listening for connections...")

    try:
        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue
                response = handle_request(data.decode("utf-8"))
                conn.send(json.dumps(response).encode("utf-8"))

    except KeyboardInterrupt:
        logging.info("userenvd shutting down (KeyboardInterrupt)")

    except Exception as e:
        logging.error(f"userenvd fatal error: {e}")
        logging.error(traceback.format_exc())

    finally:
        if os.path.exists(USERENVD_SOCKET_PATH):
            os.remove(USERENVD_SOCKET_PATH)
        logging.info("userenvd stopped.")


if __name__ == "__main__":
    setup_logging() 
    main()
