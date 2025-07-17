import os
import subprocess
import json

PLAYBOOK_DIR = os.path.abspath("playbooks")

def list_playbooks():
    print(PLAYBOOK_DIR)
    return [
        f for f in os.listdir(PLAYBOOK_DIR)
        if f.endswith(".yml") or f.endswith(".yaml")
    ]

def run_playbook(playbook_name, extra_vars):
    playbook_path = os.path.join(PLAYBOOK_DIR, playbook_name)

    if not os.path.exists(playbook_path):
        return {"error": "Playbook not found"}

    command = [
        "ansible-playbook",
        playbook_path,
        "-i", "localhost,",  # local inventory
        "--connection", "local",
        "--extra-vars", json.dumps(extra_vars),
    ]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=False
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}
