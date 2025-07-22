import os
import subprocess
import json
from typing import List
from app.models.playbook import PlaybookModel
from app.repositories.playbook_repository import PlaybookRepository
from app.extensions import redis_client
from app.config import Config

class PlaybookService:
    def __init__(self, playbook_dir=Config.PLAYBOOKS_DIR):
        self.playbook_dir = playbook_dir
        self.repo = PlaybookRepository()

    def fetch_all(self) -> List[PlaybookModel]:
        return self.repo.get_all()

    def fetch_by_user_id(self, user_id: int) -> List[PlaybookModel]:
        return self.repo.filter_by_user_id(user_id)

    def fetch_by_name(self, name: str) -> List[PlaybookModel]:
        return self.repo.filter_by_name(name)

    def fetch_by_filepath(self, filepath: str) -> List[PlaybookModel]:
        return self.repo.filter_by_filepath(filepath)

    def fetch_by_is_active(self, is_active: bool) -> List[PlaybookModel]:
        return self.repo.filter_by_is_active(is_active)

    def get_by_filepath(self, filepath) -> PlaybookModel:
        return self.repo.get_by_filepath(filepath)

    def get_by_id(self, id) -> PlaybookModel:
        return self.repo.get_by_id(id)

    def add_playbook(self, name, description, filepath, user_id):
        playbook = PlaybookModel(name=name, description=description, filepath=filepath, user_id=user_id)
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

    def stream_playbook_logs(self, playbook:PlaybookModel, extra_vars):
        playbook_path = os.path.join(self.playbook_dir, playbook.filepath)

        process = subprocess.Popen(
            ["ansible-playbook", playbook_path, "-e", json.dumps(extra_vars)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in iter(process.stdout.readline, ''):
            yield line.strip()

        process.stdout.close()
        process.wait()
