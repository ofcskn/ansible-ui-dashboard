# Playbook Manager App

A full-stack application to **manage Ansible playbooks via a web UI**.

- **Backend:** Flask + SQLAlchemy REST API
- **Frontend:** Latest Angular SPA
- **Docs:** (reserved for future documentation)

---

## Project Structure

```

Backend/ # Backend (Flask API)
├── app/
│ ├── models/
│ ├── repositories/
│ ├── routes/
│ ├── schemas/
│ ├── __init__.py
│ ├── config.py
│ └── extensions.py
├── playbooks/ # Ansible playbook YAML files
├── requirements.txt # Backend dependencies
└── main.py # Flask app entrypoint

frontend/ # Angular frontend app
docs/ # Documentation

```

---

## Features

- Manage Playbooks (create, update, delete) through REST API
- Execute Ansible playbooks on-demand with parameters
- Angular frontend to list and control playbooks interactively
- Modular and scalable code structure for easy extension

---

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm/yarn
- PostgreSQL (or compatible database)
- Ansible installed on your system (for running playbooks)

---

## Backend Setup (Flask + PostgreSQL)

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

# Run Flask backend server
flask run # or python main.py
```

---

### Windows (PowerShell)

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

## Frontend Setup (Angular)

```bash
cd frontend

# Install dependencies
npm install

# Run Angular development server
npm start
```

- Frontend will be available at `http://localhost:4200` by default.
- It communicates with the backend API to manage playbooks.

---

## Notes

- Ensure **Ansible** is installed and properly configured on your backend machine to run playbooks.
- Playbook YAML files should be placed in the `playbooks/` folder in the backend root.
- Update database connection string in `DATABASE_URL` accordingly.
- Use Postman or similar tools to test backend API endpoints during development.

---

## Future Improvements

- Add comprehensive API documentation in `/docs`
- Implement user authentication & authorization
- Dockerize backend and frontend for easy deployment
- Add advanced playbook scheduling and logging

---

## License

MIT License

---

## Contact

For questions or contributions, please open an issue or reach out via info@ofcskn.com.

---
