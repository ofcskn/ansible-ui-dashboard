# Playbook Manager App

A full-stack application to **manage Ansible playbooks via a web UI**.

- **Backend:** Flask + SQLAlchemy REST API + Privileged daemon via Unix socket
- **Frontend:** Latest Angular SPA
- **Docs:** (reserved for future documentation)

---

## Project Structure

```
Backend/ # Backend (Flask API)
├── app/
│ ├── decorators/
│ ├── helpers/
│ ├── models/
│ ├── repositories/
│ ├── routes/
│ ├── schemas/
│ ├── utils/
│ ├── __init__.py
│ ├── config.py
│ └── extensions.py
├── playbooks/ # Ansible playbook YAML files
├── migrations/ # SQL migrations
├── requirements.txt # Backend dependencies
└── main.py # Flask app entrypoint and Unix socket integration client

frontend/ # Angular frontend app
docs/ # Documentation
```

---

## Features

- Manage Playbooks (create, update, delete) through REST API
- Execute Ansible playbooks on-demand with parameters
- Angular frontend to list and control playbooks interactively
- Modular and scalable code structure for easy extension
- **User environment creation handled securely via a privileged Unix socket daemon**

---

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm/yarn
- PostgreSQL (or compatible database)
- Ansible installed on your system (for running playbooks)
- **Systemd service running the privileged daemon (`userenvd.service`) listening on Unix socket `/var/run/userenvd/socket`**

---

## Backend Setup (Flask + PostgreSQL + Unix Socket Integration)

### Linux / macOS

```bash
# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (adjust as needed)
export FLASK_APP=main.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:password@localhost:5432/playbookmanagerapp

# Create database (replace credentials accordingly)
createdb playbookmanagerapp

# Initialize migrations and create tables
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Ensure /opt/users directory exists with proper permissions:
sudo mkdir -p /opt/users
sudo chown root:root /opt/users
sudo chmod 755 /opt/users

# Make sure userenvd.service is installed and running:
sudo systemctl start userenvd.service
sudo systemctl enable userenvd.service

# Verify userenvd socket permissions:
ls -ld /var/run/userenvd
ls -l /var/run/userenvd/socket

# Flask backend server:
flask run  # or python main.py
```

---

### Windows (PowerShell)

> **Note:** Unix domain sockets and privileged daemons are Linux/macOS features. Running userenvd with socket-based isolation is **not supported on Windows** without WSL or similar. Use Linux/macOS for full features.

```powershell
# Create & activate virtual environment
python -m venv venv
venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (adjust as needed)
$env:FLASK_APP = "main.py"
$env:FLASK_ENV = "development"
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/playbookdb"

# Create USER_WORKSPACE_ROOT manually (use WSL or Linux environment)
sudo mkdir -p /opt/users
sudo chown root:root /opt/users
sudo chmod 755 /opt/users

# Create database (use psql or pgAdmin)
createdb playbookdb

# Initialize migrations and create tables
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run Flask backend server
flask run
```

---

## How User Environment Creation Works Securely

- Your **Flask API** calls the **privileged daemon** over a **raw Unix domain socket** (`/var/run/userenvd/socket`).
- This daemon runs as root and is responsible for creating isolated user directories under `/opt/users/<username>` with strict permissions.
- The Flask API sends JSON requests like:

```json
{ "username": "exampleuser" }
```

- The daemon handles creation securely and returns a JSON response with success or error.
- This approach **isolates privileged operations** away from Flask and protects the system from injection or hacking risks.

---

## Flask API Integration Example

Your Flask app can use this helper function to communicate with the daemon:

```python
import socket
import json

def call_userenvd(username: str) -> dict:
    sock_path = "/var/run/userenvd/socket"
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_path)
        client.send(json.dumps({"username": username}).encode())
        response = client.recv(4096).decode()
        client.close()
        return json.loads(response)
    except Exception as e:
        return {"status": "error", "message": f"Failed to contact userenvd: {str(e)}"}
```

Use it in your user registration or environment creation endpoints to securely provision user folders.

---

## Frontend Setup (Angular)

```bash
cd frontend

# Install dependencies
npm install

# Run Angular development server
npm start
```

- Frontend available at `http://localhost:4200`
- Communicates with backend API to manage playbooks and trigger user environment setup.

---

## Notes

- The privileged daemon (`userenvd`) **must be installed as a systemd service and running** before Flask API attempts to create user environments.
- Make sure socket file permissions allow the Flask user to connect.
- Playbook YAML files go under `/playbooks` in backend root.
- Modify `/opt/users` permissions carefully to maintain security.

---

## Future Improvements

- Add comprehensive API docs in `/docs`
- Add user authentication & role-based authorization
- Dockerize backend and frontend
- Advanced playbook scheduling & auditing

---

## License

MIT License

---

## Contact

For questions or contributions, open an issue or contact [info@ofcskn.com](mailto:info@ofcskn.com).
