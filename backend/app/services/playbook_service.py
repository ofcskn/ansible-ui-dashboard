import os
import subprocess
import json
from app.models.playbook import PlaybookModel

class PlaybookService:
    def __init__(self, playbook_dir=None):
        self.playbook_dir = playbook_dir or os.path.abspath("playbooks")

    def list_playbooks(self):
        playbooks = []
        try:
            files = [
                f for f in os.listdir(self.playbook_dir)
                if f.endswith(".yml") or f.endswith(".yaml")
            ]
            for i, filename in enumerate(files, 1):
                playbooks.append(PlaybookModel(id=i, name=filename, description=""))
        except FileNotFoundError:
            return playbooks
        return playbooks

    def run_playbook(self, playbook_name, extra_vars):
        playbook_path = os.path.join(self.playbook_dir, playbook_name)

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
