import os
import subprocess
import json
from app.models.playbook import PlaybookModel
from app.repositories.playbook_repository import PlaybookRepository
from app.constants import PLAYBOOKS_DIR
from app.extensions import redis_client

class PlaybookService:
    def __init__(self, playbook_dir=PLAYBOOKS_DIR):
        self.playbook_dir = playbook_dir
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

    def run_playbook(self, playbook:PlaybookModel, extra_vars):
        redis_client.set(f"playbook:{playbook.id}:running", "running", ex=1800)
        playbook_path = os.path.join(self.playbook_dir, playbook.filepath)

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
        finally:
            redis_client.delete(f"playbook:{str(playbook.id)}:running")