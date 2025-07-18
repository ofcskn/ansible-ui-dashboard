import os
import subprocess
import json
from app.models.playbook import PlaybookModel
from app.repositories.playbook_repository import PlaybookRepository

class PlaybookService:
    def __init__(self, playbook_dir=None):
        self.playbook_dir = playbook_dir or os.path.abspath("playbooks")
        self.repo = PlaybookRepository()

    def list_playbooks(self):
        return self.repo.get_all()

    def get_playbook(self, name) -> PlaybookModel:
        return self.repo.get_by_name(name)
    
    def get_by_id(self, id) -> PlaybookModel:
        return self.repo.get_by_id(id)

    def add_playbook(self, name, description, filepath):
        playbook = PlaybookModel(name=name, description=description, filepath=filepath)
        return self.repo.add(playbook)

    def delete_playbook(self, playbook):
        if playbook:
            self.repo.delete(playbook)
            return True
        return False

    def update_playbook(self, playbook, **kwargs):
        if not playbook:
            return None
        for key, value in kwargs.items():
            setattr(playbook, key, value)
        self.repo.update()
        return playbook

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
